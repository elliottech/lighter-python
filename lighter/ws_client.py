"""Async-first WebSocket client for the Lighter API.

This module wraps the :mod:`websockets` library to expose a high-level
interface around the channels documented at
https://apidocs.lighter.xyz/docs/websocket-reference.

Supported channels include order book, ticker, market stats, trades,
candles, account-scoped streams, pool data, height, and notifications. The
client can also send transactions over the ``jsonapi/sendtx`` and
``jsonapi/sendtxbatch`` envelopes.

Backwards compatibility is preserved with the prior client: instances can
still be constructed with ``order_book_ids`` / ``account_ids`` /
``on_order_book_update`` / ``on_account_update`` and driven with
:meth:`WsClient.run` or :meth:`WsClient.run_async`.
"""

from __future__ import annotations

import asyncio
import json
import logging
from contextlib import suppress
from typing import (
    Any,
    Awaitable,
    Callable,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Union,
)

try:
    from websockets.asyncio.client import connect as _ws_connect
except ImportError:  # pragma: no cover - websockets 12.x fallback
    from websockets.client import connect as _ws_connect

from lighter.configuration import Configuration

logger = logging.getLogger(__name__)

# Public callback type alias - callbacks may be either sync or async.
Callback = Callable[..., Union[None, Awaitable[None]]]

# Channels that require an ``auth`` token alongside the subscribe message.
_AUTH_REQUIRED_PREFIXES: Tuple[str, ...] = (
    "account_market/",
    "account_tx/",
    "account_all_orders/",
    "account_orders/",
    "account_all_assets/",
    "account_spot_avg_entry_prices/",
    "notification/",
    "pool_data/",
    "pool_info/",
)

# Subscriptions passed to the constructor as a plain channel string or a
# ``(channel, auth)`` tuple.
SubscriptionSpec = Union[str, Tuple[str, Optional[str]]]


class WsClient:
    """High-level async WebSocket client for the Lighter API.

    Parameters
    ----------
    host
        Hostname of the Lighter API (without scheme). Defaults to the host
        of :class:`lighter.Configuration`.
    path
        WebSocket path (default ``"/stream"``).
    readonly
        If ``True`` connect with the ``?readonly=true`` query parameter so
        the server allows read-only data from restricted regions.
    auth
        Default auth token used for channels that require authentication
        when no per-subscription token is provided.
    order_book_ids
        Convenience: list of market indices to subscribe to ``order_book``.
    account_ids
        Convenience: list of account indices to subscribe to ``account_all``.
    subscriptions
        Additional channels to subscribe to on connect. Each item is either
        a channel string (e.g. ``"trade/0"``, ``"candle/0/1m"``,
        ``"market_stats/all"``) or a ``(channel, auth)`` tuple.
    ping_interval, ping_timeout
        Forwarded to :func:`websockets.connect` to keep the connection
        alive. The Lighter server closes connections that send no frames
        for two minutes, so ``ping_interval`` should remain well below
        that.
    auto_reconnect
        If ``True``, the run loop reconnects when the connection drops.
    reconnect_delay
        Seconds to wait between reconnect attempts.
    on_*
        Optional callbacks (sync or async) invoked when an update for the
        corresponding channel arrives. Each callback receives the natural
        identifier(s) for the channel followed by the full server message.
    """

    DEFAULT_PATH = "/stream"

    def __init__(
        self,
        host: Optional[str] = None,
        path: str = DEFAULT_PATH,
        *,
        readonly: bool = False,
        auth: Optional[str] = None,
        order_book_ids: Optional[Iterable[int]] = None,
        account_ids: Optional[Iterable[int]] = None,
        subscriptions: Optional[Iterable[SubscriptionSpec]] = None,
        ping_interval: Optional[float] = 30.0,
        ping_timeout: Optional[float] = 60.0,
        auto_reconnect: bool = False,
        reconnect_delay: float = 1.0,
        on_order_book_update: Optional[Callback] = None,
        on_account_update: Optional[Callback] = None,
        on_ticker_update: Optional[Callback] = None,
        on_market_stats_update: Optional[Callback] = None,
        on_spot_market_stats_update: Optional[Callback] = None,
        on_trade_update: Optional[Callback] = None,
        on_candle_update: Optional[Callback] = None,
        on_account_market_update: Optional[Callback] = None,
        on_account_all_orders_update: Optional[Callback] = None,
        on_account_orders_update: Optional[Callback] = None,
        on_account_all_trades_update: Optional[Callback] = None,
        on_account_all_positions_update: Optional[Callback] = None,
        on_account_all_assets_update: Optional[Callback] = None,
        on_account_spot_avg_entry_prices_update: Optional[Callback] = None,
        on_account_tx_update: Optional[Callback] = None,
        on_user_stats_update: Optional[Callback] = None,
        on_notification_update: Optional[Callback] = None,
        on_pool_data_update: Optional[Callback] = None,
        on_pool_info_update: Optional[Callback] = None,
        on_height_update: Optional[Callback] = None,
        on_tx_response: Optional[Callback] = None,
        on_message: Optional[Callback] = None,
    ) -> None:
        if host is None:
            default_host = Configuration.get_default().host
            host = default_host.replace("https://", "").replace("http://", "")

        self.host = host
        self.path = path
        self.readonly = readonly
        self.auth = auth
        self.ping_interval = ping_interval
        self.ping_timeout = ping_timeout
        self.auto_reconnect = auto_reconnect
        self.reconnect_delay = reconnect_delay

        query = "?readonly=true" if readonly else ""
        self.base_url = f"wss://{host}{path}{query}"

        # Map of channel -> optional explicit auth token to send on subscribe.
        self._subscriptions: Dict[str, Optional[str]] = {}

        for market_id in order_book_ids or []:
            self._subscriptions[f"order_book/{int(market_id)}"] = None
        for account_id in account_ids or []:
            self._subscriptions[f"account_all/{int(account_id)}"] = None
        for spec in subscriptions or []:
            channel, token = _normalize_subscription(spec)
            self._subscriptions[channel] = token

        # Locally cached state. ``order_book_states`` reflects the merged
        # snapshot+diffs for each market, while ``account_states`` mirrors
        # the most recent ``account_all`` payload.
        self.order_book_states: Dict[int, Dict[str, List[Dict[str, Any]]]] = {}
        self.account_states: Dict[int, Dict[str, Any]] = {}

        self.on_order_book_update = on_order_book_update
        self.on_account_update = on_account_update
        self.on_ticker_update = on_ticker_update
        self.on_market_stats_update = on_market_stats_update
        self.on_spot_market_stats_update = on_spot_market_stats_update
        self.on_trade_update = on_trade_update
        self.on_candle_update = on_candle_update
        self.on_account_market_update = on_account_market_update
        self.on_account_all_orders_update = on_account_all_orders_update
        self.on_account_orders_update = on_account_orders_update
        self.on_account_all_trades_update = on_account_all_trades_update
        self.on_account_all_positions_update = on_account_all_positions_update
        self.on_account_all_assets_update = on_account_all_assets_update
        self.on_account_spot_avg_entry_prices_update = (
            on_account_spot_avg_entry_prices_update
        )
        self.on_account_tx_update = on_account_tx_update
        self.on_user_stats_update = on_user_stats_update
        self.on_notification_update = on_notification_update
        self.on_pool_data_update = on_pool_data_update
        self.on_pool_info_update = on_pool_info_update
        self.on_height_update = on_height_update
        self.on_tx_response = on_tx_response
        self.on_message = on_message

        self.ws: Optional[Any] = None
        self._send_lock: Optional[asyncio.Lock] = None
        self._stopped = False

    # ------------------------------------------------------------------
    # Subscription registration (pre-connect, synchronous)
    # ------------------------------------------------------------------

    def add_subscription(
        self, channel: str, *, auth: Optional[str] = None
    ) -> None:
        """Queue a channel to be subscribed to once :meth:`run_async` connects."""
        self._subscriptions[channel] = auth

    def add_order_book(self, market_id: int) -> None:
        self.add_subscription(f"order_book/{int(market_id)}")

    def add_ticker(self, market_id: int) -> None:
        self.add_subscription(f"ticker/{int(market_id)}")

    def add_market_stats(self, market_id: Union[int, str] = "all") -> None:
        self.add_subscription(f"market_stats/{market_id}")

    def add_spot_market_stats(self, market_id: Union[int, str] = "all") -> None:
        self.add_subscription(f"spot_market_stats/{market_id}")

    def add_trade(self, market_id: int) -> None:
        self.add_subscription(f"trade/{int(market_id)}")

    def add_candle(self, market_id: int, resolution: str) -> None:
        self.add_subscription(f"candle/{int(market_id)}/{resolution}")

    def add_height(self) -> None:
        self.add_subscription("height")

    def add_account_all(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(f"account_all/{int(account_id)}", auth=auth)

    def add_account_market(
        self,
        market_id: int,
        account_id: int,
        *,
        auth: Optional[str] = None,
    ) -> None:
        self.add_subscription(
            f"account_market/{int(market_id)}/{int(account_id)}", auth=auth
        )

    def add_account_all_orders(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(
            f"account_all_orders/{int(account_id)}", auth=auth
        )

    def add_account_orders(
        self,
        market_id: int,
        account_id: int,
        *,
        auth: Optional[str] = None,
    ) -> None:
        self.add_subscription(
            f"account_orders/{int(market_id)}/{int(account_id)}", auth=auth
        )

    def add_account_all_trades(self, account_id: int) -> None:
        self.add_subscription(f"account_all_trades/{int(account_id)}")

    def add_account_all_positions(self, account_id: int) -> None:
        self.add_subscription(f"account_all_positions/{int(account_id)}")

    def add_account_all_assets(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(
            f"account_all_assets/{int(account_id)}", auth=auth
        )

    def add_account_spot_avg_entry_prices(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(
            f"account_spot_avg_entry_prices/{int(account_id)}", auth=auth
        )

    def add_account_tx(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(f"account_tx/{int(account_id)}", auth=auth)

    def add_user_stats(self, account_id: int) -> None:
        self.add_subscription(f"user_stats/{int(account_id)}")

    def add_notification(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(f"notification/{int(account_id)}", auth=auth)

    def add_pool_data(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(f"pool_data/{int(account_id)}", auth=auth)

    def add_pool_info(
        self, account_id: int, *, auth: Optional[str] = None
    ) -> None:
        self.add_subscription(f"pool_info/{int(account_id)}", auth=auth)

    @property
    def subscriptions(self) -> Dict[str, Optional[str]]:
        """A copy of the registered subscriptions (channel -> auth token)."""
        return dict(self._subscriptions)

    # ------------------------------------------------------------------
    # Async send helpers (runtime)
    # ------------------------------------------------------------------

    async def send_json(self, message: Mapping[str, Any]) -> None:
        """Send a JSON-encoded message on the open WebSocket connection."""
        ws = self.ws
        if ws is None:
            raise RuntimeError("WebSocket is not connected")
        if self._send_lock is None:
            self._send_lock = asyncio.Lock()
        async with self._send_lock:
            await ws.send(json.dumps(message))

    async def subscribe(
        self, channel: str, auth: Optional[str] = None
    ) -> None:
        """Subscribe to ``channel`` at runtime.

        The subscription is also remembered so that it will be re-sent if
        :attr:`auto_reconnect` triggers a reconnect.
        """
        token = auth if auth is not None else self._auth_for_channel(channel)
        payload: Dict[str, Any] = {"type": "subscribe", "channel": channel}
        if token is not None:
            payload["auth"] = token
        await self.send_json(payload)
        self._subscriptions[channel] = auth

    async def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from ``channel`` at runtime and drop any cached state."""
        await self.send_json({"type": "unsubscribe", "channel": channel})
        self._subscriptions.pop(channel, None)
        if channel.startswith("order_book/"):
            with suppress(ValueError):
                market_id = int(channel.split("/", 1)[1])
                self.order_book_states.pop(market_id, None)
        elif channel.startswith("account_all/"):
            with suppress(ValueError):
                account_id = int(channel.split("/", 1)[1])
                self.account_states.pop(account_id, None)

    async def send_tx(
        self,
        tx_type: int,
        tx_info: Union[str, Mapping[str, Any]],
        *,
        id: Optional[str] = None,
    ) -> None:
        """Send a signed transaction via ``jsonapi/sendtx``.

        ``tx_info`` may be the JSON-encoded string returned by the signer
        helpers or an already-parsed mapping.
        """
        data: Dict[str, Any] = {
            "tx_type": int(tx_type),
            "tx_info": _decode_tx_info(tx_info),
        }
        if id is not None:
            data["id"] = id
        await self.send_json({"type": "jsonapi/sendtx", "data": data})

    async def send_tx_batch(
        self,
        tx_types: Iterable[int],
        tx_infos: Iterable[Union[str, Mapping[str, Any]]],
        *,
        id: Optional[str] = None,
    ) -> None:
        """Send a batch of signed transactions via ``jsonapi/sendtxbatch``.

        The server expects ``tx_types`` and ``tx_infos`` as JSON-encoded
        string arrays; this method matches that wire format so it accepts
        the same ``tx_info`` strings produced by the signer helpers.
        """
        info_strings: List[str] = []
        for info in tx_infos:
            if isinstance(info, str):
                info_strings.append(info)
            else:
                info_strings.append(json.dumps(info))
        data: Dict[str, Any] = {
            "tx_types": json.dumps([int(t) for t in tx_types]),
            "tx_infos": json.dumps(info_strings),
        }
        if id is not None:
            data["id"] = id
        await self.send_json({"type": "jsonapi/sendtxbatch", "data": data})

    def _auth_for_channel(self, channel: str) -> Optional[str]:
        stored = self._subscriptions.get(channel)
        if stored is not None:
            return stored
        if channel.startswith(_AUTH_REQUIRED_PREFIXES):
            return self.auth
        return None

    # ------------------------------------------------------------------
    # Run loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        """Synchronous wrapper that drives :meth:`run_async` to completion."""
        asyncio.run(self.run_async())

    async def run_async(self) -> None:
        """Connect, dispatch messages, and (optionally) reconnect on errors."""
        self._stopped = False
        while not self._stopped:
            try:
                await self._connect_and_consume()
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                if not self.auto_reconnect or self._stopped:
                    raise
                logger.warning(
                    "WebSocket disconnected: %s; reconnecting in %.1fs",
                    exc,
                    self.reconnect_delay,
                )
                await asyncio.sleep(self.reconnect_delay)
                continue
            if not self.auto_reconnect:
                return

    async def close(self) -> None:
        """Stop the run loop and close the WebSocket connection."""
        self._stopped = True
        ws = self.ws
        if ws is not None:
            with suppress(Exception):
                await ws.close()

    async def _connect_and_consume(self) -> None:
        async with _ws_connect(
            self.base_url,
            ping_interval=self.ping_interval,
            ping_timeout=self.ping_timeout,
        ) as ws:
            self.ws = ws
            self._send_lock = asyncio.Lock()
            try:
                await self._send_all_subscriptions()
                async for raw in ws:
                    if isinstance(raw, bytes):
                        # Lighter sends JSON text; ignore unexpected binary
                        # frames so callers can still rely on dict payloads.
                        logger.debug("Ignoring binary WebSocket frame")
                        continue
                    await self._dispatch(json.loads(raw))
            finally:
                self.ws = None
                self._send_lock = None

    async def _send_all_subscriptions(self) -> None:
        for channel, explicit_auth in list(self._subscriptions.items()):
            payload: Dict[str, Any] = {"type": "subscribe", "channel": channel}
            token = (
                explicit_auth
                if explicit_auth is not None
                else self._auth_for_channel(channel)
            )
            if token is not None:
                payload["auth"] = token
            await self.send_json(payload)

    # ------------------------------------------------------------------
    # Message dispatch
    # ------------------------------------------------------------------

    async def _dispatch(self, message: Dict[str, Any]) -> None:
        message_type = message.get("type", "")

        if message_type == "ping":
            await self.send_json({"type": "pong"})
            return
        if message_type == "pong":
            return
        if message_type == "connected":
            # The server's welcome message arrives once per connection.
            # Subscriptions are already sent eagerly on connect.
            await self._call(self.on_message, message)
            return
        if message_type.startswith("jsonapi/"):
            await self._call(self.on_tx_response, message)
            return

        kind = _channel_kind(message_type)
        if kind is None:
            await self._call(self.on_message, message)
            return

        handler = getattr(self, f"_handle_{kind}", None)
        if handler is None:
            await self._call(self.on_message, message)
            return
        await handler(message)

    # ------------------------------------------------------------------
    # Per-channel handlers
    # ------------------------------------------------------------------

    async def _handle_order_book(self, message: Dict[str, Any]) -> None:
        market_id = _parse_id(message.get("channel", ""))
        if market_id is None:
            return
        order_book = message.get("order_book") or {}
        if message.get("type") == "subscribed/order_book":
            self.order_book_states[market_id] = {
                "asks": list(order_book.get("asks") or []),
                "bids": list(order_book.get("bids") or []),
            }
        else:
            state = self.order_book_states.setdefault(
                market_id, {"asks": [], "bids": []}
            )
            _apply_order_book_diff(
                order_book.get("asks") or [], state["asks"]
            )
            _apply_order_book_diff(
                order_book.get("bids") or [], state["bids"]
            )
        await self._call(
            self.on_order_book_update,
            market_id,
            self.order_book_states[market_id],
        )

    async def _handle_account_all(self, message: Dict[str, Any]) -> None:
        account_id = _parse_id(message.get("channel", ""))
        if account_id is None:
            return
        self.account_states[account_id] = message
        await self._call(self.on_account_update, account_id, message)

    async def _handle_ticker(self, message: Dict[str, Any]) -> None:
        market_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_ticker_update, market_id, message)

    async def _handle_market_stats(self, message: Dict[str, Any]) -> None:
        key = _parse_key(message.get("channel", ""))
        await self._call(self.on_market_stats_update, key, message)

    async def _handle_spot_market_stats(
        self, message: Dict[str, Any]
    ) -> None:
        key = _parse_key(message.get("channel", ""))
        await self._call(self.on_spot_market_stats_update, key, message)

    async def _handle_trade(self, message: Dict[str, Any]) -> None:
        market_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_trade_update, market_id, message)

    async def _handle_candle(self, message: Dict[str, Any]) -> None:
        market_id, resolution = _parse_candle_channel(message.get("channel", ""))
        await self._call(
            self.on_candle_update, market_id, resolution, message
        )

    async def _handle_account_market(self, message: Dict[str, Any]) -> None:
        market_id, account_id = _parse_two_ids(message.get("channel", ""))
        await self._call(
            self.on_account_market_update, market_id, account_id, message
        )

    async def _handle_account_orders(self, message: Dict[str, Any]) -> None:
        market_id, account_id = _parse_two_ids(message.get("channel", ""))
        await self._call(
            self.on_account_orders_update, market_id, account_id, message
        )

    async def _handle_account_all_orders(
        self, message: Dict[str, Any]
    ) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(
            self.on_account_all_orders_update, account_id, message
        )

    async def _handle_account_all_trades(
        self, message: Dict[str, Any]
    ) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(
            self.on_account_all_trades_update, account_id, message
        )

    async def _handle_account_all_positions(
        self, message: Dict[str, Any]
    ) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(
            self.on_account_all_positions_update, account_id, message
        )

    async def _handle_account_all_assets(
        self, message: Dict[str, Any]
    ) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(
            self.on_account_all_assets_update, account_id, message
        )

    async def _handle_account_spot_avg_entry_prices(
        self, message: Dict[str, Any]
    ) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(
            self.on_account_spot_avg_entry_prices_update,
            account_id,
            message,
        )

    async def _handle_account_tx(self, message: Dict[str, Any]) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_account_tx_update, account_id, message)

    async def _handle_user_stats(self, message: Dict[str, Any]) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_user_stats_update, account_id, message)

    async def _handle_notification(self, message: Dict[str, Any]) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_notification_update, account_id, message)

    async def _handle_pool_data(self, message: Dict[str, Any]) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_pool_data_update, account_id, message)

    async def _handle_pool_info(self, message: Dict[str, Any]) -> None:
        account_id = _parse_id(message.get("channel", ""))
        await self._call(self.on_pool_info_update, account_id, message)

    async def _handle_height(self, message: Dict[str, Any]) -> None:
        height = message.get("height")
        await self._call(self.on_height_update, height, message)

    # ------------------------------------------------------------------
    # Callback invocation helper
    # ------------------------------------------------------------------

    async def _call(
        self, callback: Optional[Callback], *args: Any
    ) -> None:
        if callback is None:
            return
        result = callback(*args)
        if asyncio.iscoroutine(result):
            await result


# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------


def _normalize_subscription(spec: SubscriptionSpec) -> Tuple[str, Optional[str]]:
    if isinstance(spec, tuple):
        if len(spec) != 2:
            raise ValueError(
                "subscription tuples must have the form (channel, auth_token)"
            )
        channel, token = spec
        return str(channel), token
    return str(spec), None


def _channel_kind(message_type: str) -> Optional[str]:
    """Return the channel kind for ``subscribed/<kind>`` and ``update/<kind>``."""
    if not message_type:
        return None
    for prefix in ("subscribed/", "update/"):
        if message_type.startswith(prefix):
            return message_type[len(prefix):]
    return None


def _channel_body(channel: str) -> List[str]:
    """Return the parts of the channel that follow the leading name.

    Channel strings appear with either ``/`` or ``:`` separators depending on
    whether they come from a subscribe request or a server response.
    """
    if not channel:
        return []
    normalized = channel.replace("/", ":")
    parts = normalized.split(":")
    if len(parts) <= 1:
        return []
    return parts[1:]


def _parse_id(channel: str) -> Optional[int]:
    parts = _channel_body(channel)
    if not parts:
        return None
    try:
        return int(parts[0])
    except ValueError:
        return None


def _parse_key(channel: str) -> Union[int, str, None]:
    parts = _channel_body(channel)
    if not parts:
        return None
    value = parts[0]
    try:
        return int(value)
    except ValueError:
        return value


def _parse_two_ids(
    channel: str,
) -> Tuple[Optional[int], Optional[int]]:
    parts = _channel_body(channel)
    first: Optional[int] = None
    second: Optional[int] = None
    if len(parts) >= 1:
        with suppress(ValueError):
            first = int(parts[0])
    if len(parts) >= 2:
        with suppress(ValueError):
            second = int(parts[1])
    return first, second


def _parse_candle_channel(
    channel: str,
) -> Tuple[Optional[int], Optional[str]]:
    parts = _channel_body(channel)
    market_id: Optional[int] = None
    resolution: Optional[str] = None
    if len(parts) >= 1:
        with suppress(ValueError):
            market_id = int(parts[0])
    if len(parts) >= 2:
        resolution = parts[1]
    return market_id, resolution


def _decode_tx_info(
    tx_info: Union[str, Mapping[str, Any]],
) -> Any:
    if isinstance(tx_info, str):
        return json.loads(tx_info)
    return dict(tx_info)


def _apply_order_book_diff(
    new_orders: List[Dict[str, Any]],
    existing_orders: List[Dict[str, Any]],
) -> None:
    """Merge ``new_orders`` into ``existing_orders`` in-place using price as key.

    Entries with size ``0`` remove the corresponding price level. The order
    of the resulting list reflects the underlying dict insertion order so it
    is not guaranteed to be sorted; consumers that need a sorted book should
    sort by ``price`` after each update.
    """
    by_price: Dict[str, Dict[str, Any]] = {
        order["price"]: order for order in existing_orders
    }
    for new_order in new_orders:
        price = new_order["price"]
        try:
            size = float(new_order["size"])
        except (TypeError, ValueError):
            size = 0.0
        if size == 0:
            by_price.pop(price, None)
        else:
            by_price[price] = new_order
    existing_orders[:] = list(by_price.values())
