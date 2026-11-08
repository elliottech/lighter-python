import json
from bisect import bisect_left
from decimal import Decimal
from websockets.sync.client import connect
from websockets.client import connect as connect_async
from lighter.configuration import Configuration
from lighter.endpoint_profiles import join_url
import logging
logger = logging.getLogger(__name__)

class WsClient:
    def __init__(
        self,
        host=None,
        path="/stream",
        order_book_ids=[],
        account_ids=[],
        on_order_book_update=print,
        on_account_update=print,
        ws_url=None,
        on_shutdown=None,
        on_unhandled_message=None,
        on_order_book_gap=None,
        verify_order_book_continuity=True,
    ):
        if ws_url is not None:
            self.base_url = ws_url.rstrip("/")
        else:
            if host is None:
                host = Configuration.get_default().host.replace("https://", "")
            self.base_url = join_url(f"wss://{host}", path)

        self.subscriptions = {
            "order_books": order_book_ids,
            "accounts": account_ids,
        }

        if len(order_book_ids) == 0 and len(account_ids) == 0:
            raise Exception("No subscriptions provided.")

        self.order_book_states = {}
        self.account_states = {}
        # Sorted price keys per market and side, kept parallel to the level lists in
        # order_book_states (asks ascending, bids descending), so updates are O(log n).
        self._order_book_keys = {}
        # Markets whose book broke continuity and are waiting for a fresh snapshot.
        self._resyncing_markets = set()
        self._pending_resyncs = []
        self._async_mode = False

        self.on_order_book_update = on_order_book_update
        self.on_account_update = on_account_update
        self.on_shutdown = on_shutdown
        self.on_unhandled_message = on_unhandled_message
        self.on_order_book_gap = on_order_book_gap
        self.verify_order_book_continuity = verify_order_book_continuity

        self.ws = None

    def on_message(self, ws, message):
        if isinstance(message, str):
            message = json.loads(message)

        message_type = message.get("type")

        if message_type == "connected":
            self.handle_connected(ws)
        elif message_type == "subscribed/order_book":
            self.handle_subscribed_order_book(message)
        elif message_type == "update/order_book":
            self.handle_update_order_book(message)
        elif message_type == "subscribed/account_all":
            self.handle_subscribed_account(message)
        elif message_type == "update/account_all":
            self.handle_update_account(message)
        elif message_type == "ping":
            # Respond to ping with pong
            ws.send(json.dumps({"type": "pong"}))
        elif message_type == "shutdown":
            self.handle_shutdown(message)
        elif message_type == "unsubscribed" and self._is_resync_ack(message):
            pass
        else:
            self.handle_unhandled_message(message)

        if not self._async_mode:
            self._flush_resyncs(ws)

    async def on_message_async(self, ws, message):
        message = json.loads(message)
        message_type = message.get("type")

        if message_type == "connected":
            await self.handle_connected_async(ws)
        elif message_type == "ping":
            # Respond to ping with pong
            await ws.send(json.dumps({"type": "pong"}))
        else:
            self._async_mode = True
            self.on_message(ws, message)
            await self._flush_resyncs_async(ws)

    def handle_connected(self, ws):
        for market_id in self.subscriptions["order_books"]:
            ws.send(
                json.dumps({"type": "subscribe", "channel": f"order_book/{market_id}"})
            )
        for account_id in self.subscriptions["accounts"]:
            ws.send(
                json.dumps(
                    {"type": "subscribe", "channel": f"account_all/{account_id}"}
                )
            )

    async def handle_connected_async(self, ws):
        for market_id in self.subscriptions["order_books"]:
            await ws.send(
                json.dumps({"type": "subscribe", "channel": f"order_book/{market_id}"})
            )
        for account_id in self.subscriptions["accounts"]:
            await ws.send(
                json.dumps(
                    {"type": "subscribe", "channel": f"account_all/{account_id}"}
                )
            )

    def handle_subscribed_order_book(self, message):
        market_id = message["channel"].split(":")[1]
        order_book = message["order_book"]
        # The snapshot replaces any previous book, including one that lost continuity.
        self._resyncing_markets.discard(market_id)
        order_book["asks"] = [o for o in order_book.get("asks", []) if Decimal(o["size"]) > 0]
        order_book["bids"] = [o for o in order_book.get("bids", []) if Decimal(o["size"]) > 0]
        order_book["asks"].sort(key=lambda o: Decimal(o["price"]))
        order_book["bids"].sort(key=lambda o: -Decimal(o["price"]))
        self._order_book_keys[market_id] = {
            "asks": [Decimal(o["price"]) for o in order_book["asks"]],
            "bids": [-Decimal(o["price"]) for o in order_book["bids"]],
        }
        self.order_book_states[market_id] = order_book
        if self.on_order_book_update:
            self.on_order_book_update(market_id, self.order_book_states[market_id])

    def handle_update_order_book(self, message):
        market_id = message["channel"].split(":")[1]
        if market_id in self._resyncing_markets or market_id not in self.order_book_states:
            # Waiting for a fresh snapshot; deltas on a broken book would be wrong.
            return
        order_book = message["order_book"]
        if self.verify_order_book_continuity and not self._is_continuous(market_id, order_book):
            self._handle_order_book_gap(market_id, order_book)
            return
        self.update_order_book_state(market_id, order_book)
        if self.on_order_book_update:
            self.on_order_book_update(market_id, self.order_book_states[market_id])

    def _is_continuous(self, market_id, order_book):
        """Lighter's documented check: an update's begin_nonce equals the previous nonce."""
        expected = self.order_book_states[market_id].get("nonce")
        begin = order_book.get("begin_nonce")
        if expected is None or begin is None:
            return True
        return begin == expected

    def _handle_order_book_gap(self, market_id, order_book):
        expected = self.order_book_states[market_id].get("nonce")
        got = order_book.get("begin_nonce")
        logger.warning(
            "Order book %s lost continuity (expected begin_nonce %s, got %s); resubscribing for a fresh snapshot",
            market_id, expected, got,
        )
        self._resyncing_markets.add(market_id)
        self._pending_resyncs.append(market_id)
        if self.on_order_book_gap:
            self.on_order_book_gap(market_id, expected, got)

    def _is_resync_ack(self, message):
        """True for the server's ack of an unsubscribe we sent while resyncing a book."""
        channel = message.get("channel", "")
        return channel.startswith("order_book:") and channel.split(":")[1] in self._resyncing_markets

    def _resync_messages(self, market_id):
        channel = f"order_book/{market_id}"
        return [
            json.dumps({"type": "unsubscribe", "channel": channel}),
            json.dumps({"type": "subscribe", "channel": channel}),
        ]

    def _flush_resyncs(self, ws):
        while self._pending_resyncs:
            for payload in self._resync_messages(self._pending_resyncs.pop(0)):
                ws.send(payload)

    async def _flush_resyncs_async(self, ws):
        while self._pending_resyncs:
            for payload in self._resync_messages(self._pending_resyncs.pop(0)):
                await ws.send(payload)

    def update_order_book_state(self, market_id, order_book):
        state = self.order_book_states[market_id]
        keys = self._order_book_keys.get(market_id)
        if keys is None:
            # State set directly by the caller: index it once.
            state["asks"].sort(key=lambda o: Decimal(o["price"]))
            state["bids"].sort(key=lambda o: -Decimal(o["price"]))
            keys = self._order_book_keys[market_id] = {
                "asks": [Decimal(o["price"]) for o in state["asks"]],
                "bids": [-Decimal(o["price"]) for o in state["bids"]],
            }
        self._apply_levels(order_book.get("asks", []), state["asks"], keys["asks"], 1)
        self._apply_levels(order_book.get("bids", []), state["bids"], keys["bids"], -1)
        for field in ("nonce", "begin_nonce", "offset", "last_updated_at"):
            if field in order_book:
                state[field] = order_book[field]

    @staticmethod
    def _apply_levels(new_orders, levels, keys, sign):
        """Apply price-level deltas in place, keeping levels sorted (sign=1 asks, -1 bids)."""
        for new_order in new_orders:
            key = sign * Decimal(new_order["price"])
            i = bisect_left(keys, key)
            exists = i < len(keys) and keys[i] == key
            if Decimal(new_order["size"]) == 0:
                if exists:
                    del keys[i]
                    del levels[i]
            elif exists:
                levels[i]["size"] = new_order["size"]
            else:
                keys.insert(i, key)
                levels.insert(i, new_order)

    def update_orders(self, new_orders, existing_orders):
        for new_order in new_orders:
            is_new_order = True
            # iterate over a copy so removal is safe
            existing_order_copy = existing_orders[:]
            for existing_order in existing_order_copy:
                if new_order["price"] == existing_order["price"]:
                    is_new_order = False
                    existing_order["size"] = new_order["size"]
                    if float(new_order["size"]) == 0:
                        existing_orders.remove(existing_order)

            if is_new_order:
                existing_orders.append(new_order)

        # final cleanup (in-place)
        existing_orders[:] = [
            order for order in existing_orders if float(order["size"]) > 0
        ]

    def handle_subscribed_account(self, message):
        account_id = message["channel"].split(":")[1]
        self.account_states[account_id] = message
        if self.on_account_update:
            self.on_account_update(account_id, self.account_states[account_id])

    def handle_update_account(self, message):
        account_id = message["channel"].split(":")[1]
        self.account_states[account_id] = message
        if self.on_account_update:
            self.on_account_update(account_id, self.account_states[account_id])

    def handle_unhandled_message(self, message):
        if self.on_unhandled_message:
            self.on_unhandled_message(message)
        else:
            logger.warning("Unhandled message type %r: %s", message.get("type"), message)

    def handle_shutdown(self, message):
        close_in_ms = message.get("close_in_ms", 0)
        if self.on_shutdown:
            self.on_shutdown(close_in_ms)
        else:
            print(f"Server shutting down, connection closes in {close_in_ms}ms")

    def on_error(self, ws, error):
        raise Exception(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        raise Exception(f"Closed: {close_status_code} {close_msg}")

    def run(self):
        ws = connect(self.base_url)
        self.ws = ws

        for message in ws:
            self.on_message(ws, message)

    async def run_async(self):
        ws = await connect_async(self.base_url)
        self.ws = ws

        async for message in ws:
            await self.on_message_async(ws, message)
