import asyncio
import json
import threading
from websockets.sync.client import connect
from websockets import connect as connect_async
from lighter.configuration import Configuration


class WsClient:
    def __init__(
        self,
        host=None,
        path="/stream",
        order_book_ids=[],
        account_ids=[],
        on_order_book_update=print,
        on_account_update=print,
        on_gap_detected=print,
        ping_interval_seconds=90,
        verify_orderbook_nonce=True,
    ):
        if host is None:
            host = Configuration.get_default().host.replace("https://", "")

        self.base_url = f"wss://{host}{path}"

        self.subscriptions = {
            "order_books": order_book_ids,
            "accounts": account_ids,
        }

        if len(order_book_ids) == 0 and len(account_ids) == 0:
            raise Exception("No subscriptions provided.")

        self.order_book_states = {}
        self.order_book_last_nonce = {}
        self.account_states = {}

        self.on_order_book_update = on_order_book_update
        self.on_account_update = on_account_update
        self.on_gap_detected = on_gap_detected

        self.verify_orderbook_nonce = verify_orderbook_nonce
        self.ping_interval_seconds = ping_interval_seconds

        self.ws = None
        self._sync_keepalive_stop = threading.Event()

    def on_message(self, ws, message):
        if isinstance(message, str):
            message = json.loads(message)

        message_type = message.get("type")

        if message_type == "connected":
            self.handle_connected(ws)
        elif message_type == "subscribed/order_book":
            self.handle_subscribed_order_book(message)
        elif message_type == "update/order_book":
            self.handle_update_order_book(ws, message)
        elif message_type == "subscribed/account_all":
            self.handle_subscribed_account(message)
        elif message_type == "update/account_all":
            self.handle_update_account(message)
        elif message_type == "ping":
            ws.send(json.dumps({"type": "pong"}))
        else:
            self.handle_unhandled_message(message)

    async def on_message_async(self, ws, message):
        if isinstance(message, str):
            message = json.loads(message)

        if not isinstance(message, dict):
            return

        message_type = message.get("type")

        if message_type == "connected":
            await self.handle_connected_async(ws)
        elif message_type == "subscribed/order_book":
            self.handle_subscribed_order_book(message)
        elif message_type == "update/order_book":
            await self.handle_update_order_book_async(ws, message)
        elif message_type == "subscribed/account_all":
            self.handle_subscribed_account(message)
        elif message_type == "update/account_all":
            self.handle_update_account(message)
        elif message_type == "ping":
            await ws.send(json.dumps({"type": "pong"}))
        else:
            self.handle_unhandled_message(message)

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
        self.order_book_states[market_id] = message["order_book"]
        self.order_book_last_nonce[market_id] = message["order_book"].get("nonce")
        if self.on_order_book_update:
            self.on_order_book_update(market_id, self.order_book_states[market_id])

    def _nonce_gap_detected(self, market_id, order_book):
        if not self.verify_orderbook_nonce:
            return False

        begin_nonce = order_book.get("begin_nonce")
        prev_nonce = self.order_book_last_nonce.get(market_id)

        if begin_nonce is None or prev_nonce is None:
            return False

        return begin_nonce != prev_nonce

    def _resubscribe_order_book(self, ws, market_id):
        ws.send(json.dumps({"type": "subscribe", "channel": f"order_book/{market_id}"}))

    async def _resubscribe_order_book_async(self, ws, market_id):
        await ws.send(json.dumps({"type": "subscribe", "channel": f"order_book/{market_id}"}))

    def handle_update_order_book(self, ws, message):
        market_id = message["channel"].split(":")[1]
        order_book = message["order_book"]

        if self._nonce_gap_detected(market_id, order_book):
            if self.on_gap_detected:
                self.on_gap_detected(
                    {
                        "type": "order_book_nonce_gap",
                        "market_id": market_id,
                        "expected_begin_nonce": self.order_book_last_nonce.get(market_id),
                        "actual_begin_nonce": order_book.get("begin_nonce"),
                    }
                )
            self._resubscribe_order_book(ws, market_id)
            return

        self.update_order_book_state(market_id, order_book)
        self.order_book_last_nonce[market_id] = order_book.get("nonce", self.order_book_last_nonce.get(market_id))
        if self.on_order_book_update:
            self.on_order_book_update(market_id, self.order_book_states[market_id])

    async def handle_update_order_book_async(self, ws, message):
        market_id = message["channel"].split(":")[1]
        order_book = message["order_book"]

        if self._nonce_gap_detected(market_id, order_book):
            if self.on_gap_detected:
                self.on_gap_detected(
                    {
                        "type": "order_book_nonce_gap",
                        "market_id": market_id,
                        "expected_begin_nonce": self.order_book_last_nonce.get(market_id),
                        "actual_begin_nonce": order_book.get("begin_nonce"),
                    }
                )
            await self._resubscribe_order_book_async(ws, market_id)
            return

        self.update_order_book_state(market_id, order_book)
        self.order_book_last_nonce[market_id] = order_book.get("nonce", self.order_book_last_nonce.get(market_id))
        if self.on_order_book_update:
            self.on_order_book_update(market_id, self.order_book_states[market_id])

    def update_order_book_state(self, market_id, order_book):
        if market_id not in self.order_book_states:
            self.order_book_states[market_id] = order_book
            return

        self.update_orders(
            order_book["asks"], self.order_book_states[market_id]["asks"]
        )
        self.update_orders(
            order_book["bids"], self.order_book_states[market_id]["bids"]
        )

    def update_orders(self, new_orders, existing_orders):
        for new_order in new_orders:
            is_new_order = True
            existing_order_copy = existing_orders[:]
            for existing_order in existing_order_copy:
                if new_order["price"] == existing_order["price"]:
                    is_new_order = False
                    existing_order["size"] = new_order["size"]
                    if float(new_order["size"]) == 0:
                        existing_orders.remove(existing_order)

            if is_new_order:
                existing_orders.append(new_order)

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
        raise Exception(f"Unhandled message: {message}")

    def on_error(self, ws, error):
        raise Exception(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        raise Exception(f"Closed: {close_status_code} {close_msg}")

    def _sync_keepalive(self, ws):
        while not self._sync_keepalive_stop.wait(self.ping_interval_seconds):
            try:
                ws.ping()
            except Exception:
                return

    async def _async_keepalive(self, ws):
        while True:
            await asyncio.sleep(self.ping_interval_seconds)
            try:
                await ws.ping()
            except Exception:
                return

    def run(self):
        ws = connect(self.base_url)
        self.ws = ws

        self._sync_keepalive_stop.clear()
        keepalive_thread = threading.Thread(target=self._sync_keepalive, args=(ws,), daemon=True)
        keepalive_thread.start()

        try:
            for message in ws:
                self.on_message(ws, message)
        finally:
            self._sync_keepalive_stop.set()

    async def run_async(self):
        ws = await connect_async(self.base_url)
        self.ws = ws

        keepalive_task = asyncio.create_task(self._async_keepalive(ws))
        try:
            async for message in ws:
                await self.on_message_async(ws, message)
        finally:
            keepalive_task.cancel()
