"""Async WebSocket client for the Lighter API.

Implements the channels and message types documented at
https://apidocs.lighter.xyz/docs/websocket-reference.

The client exposes a single uniform :meth:`WsClient.subscribe` method for
all channels: callers pass the full channel string (e.g. ``"order_book/0"``,
``"trade/0"``, ``"candle/0/1m"``, ``"market_stats/all"``,
``"account_all/123"``) and an ``on_update`` callback. Authenticated
channels receive a default auth token from the client (overridable per
subscription).

Transaction submission is supported via :meth:`WsClient.send_tx` and
:meth:`WsClient.send_tx_batch` which wrap the ``jsonapi/sendtx`` and
``jsonapi/sendtxbatch`` envelopes.
"""

from __future__ import annotations

import asyncio
import json
import logging
from contextlib import suppress
from dataclasses import dataclass
from typing import (
    Any,
    Awaitable,
    Callable,
    Coroutine,
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


@dataclass
class _Subscription:
    """A registered channel subscription."""

    channel: str
    on_update: Optional[Callback] = None
    auth: Optional[str] = None


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
        If ``True`` connect with the ``?readonly=true`` query parameter.
    auth
        Default auth token used for channels under the documented
        auth-required prefixes when no per-subscription token is provided.
    ping_interval, ping_timeout
        Forwarded to :func:`websockets.connect` for WebSocket-level
        keepalive. The Lighter server closes connections that send no
        frames for two minutes, so ``ping_interval`` should remain well
        below that.
    auto_reconnect
        If ``True``, the run loop reconnects when the connection drops.
        Registered subscriptions are re-sent on each reconnect.
    reconnect_delay
        Seconds to wait between reconnect attempts.
    on_message
        Optional callback invoked for any server message that does not
        match a registered subscription (e.g. the ``connected`` welcome
        message or unknown channels).
    on_tx_response
        Optional callback invoked for every ``jsonapi/*`` server message
        (transaction send responses and errors).
    """

    DEFAULT_PATH = "/stream"

    def __init__(
        self,
        host: Optional[str] = None,
        *,
        path: str = DEFAULT_PATH,
        readonly: bool = False,
        auth: Optional[str] = None,
        ping_interval: Optional[float] = 30.0,
        ping_timeout: Optional[float] = 60.0,
        auto_reconnect: bool = False,
        reconnect_delay: float = 1.0,
        on_message: Optional[Callback] = None,
        on_tx_response: Optional[Callback] = None,
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
        self.on_message = on_message
        self.on_tx_response = on_tx_response

        query = "?readonly=true" if readonly else ""
        self.base_url = f"wss://{host}{path}{query}"

        # Registered subscriptions keyed by canonical channel name (using
        # ``/`` separators throughout for parity with the docs).
        self._subscriptions: Dict[str, _Subscription] = {}

        # Reconstructed order book snapshots, keyed by market_id. The
        # client merges snapshot+diff messages for any ``order_book/*``
        # subscription so that callers can read the current book without
        # having to maintain state themselves.
        self.order_book_states: Dict[int, Dict[str, List[Dict[str, Any]]]] = {}

        self.ws: Optional[Any] = None
        self._send_lock: Optional[asyncio.Lock] = None
        self._stopped = False

    # ------------------------------------------------------------------
    # Subscription management
    # ------------------------------------------------------------------

    def subscribe(
        self,
        channel: str,
        on_update: Optional[Callback] = None,
        *,
        auth: Optional[str] = None,
    ) -> None:
        """Register a subscription for ``channel``.

        The subscription is sent to the server on connect (and re-sent on
        each reconnect when :attr:`auto_reconnect` is enabled). If the
        client is already connected when :meth:`subscribe` is called the
        subscribe frame is dispatched immediately via the running event
        loop.

        ``on_update`` is invoked with the full server message dict (both
        the initial ``subscribed/...`` snapshot and subsequent
        ``update/...`` messages). The callback may be sync or async.

        ``auth`` is sent alongside the subscribe message. If omitted and
        ``channel`` is under one of the documented auth-required
        prefixes, the client's default :attr:`auth` is used.
        """
        canonical = _canonical_channel(channel)
        self._subscriptions[canonical] = _Subscription(
            channel=canonical, on_update=on_update, auth=auth
        )
        if self.ws is not None:
            self._spawn(self._send_subscribe(canonical))

    def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from ``channel`` and discard any cached state."""
        canonical = _canonical_channel(channel)
        self._subscriptions.pop(canonical, None)
        if canonical.startswith("order_book/"):
            with suppress(ValueError):
                market_id = int(canonical.split("/", 1)[1])
                self.order_book_states.pop(market_id, None)
        if self.ws is not None:
            self._spawn(
                self.send_json({"type": "unsubscribe", "channel": canonical})
            )

    @property
    def subscriptions(self) -> Mapping[str, _Subscription]:
        """A read-only view of registered subscriptions."""
        return dict(self._subscriptions)

    # ------------------------------------------------------------------
    # Sending
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

    async def send_tx(
        self,
        tx_type: int,
        tx_info: Union[str, Mapping[str, Any]],
        *,
        id: Optional[str] = None,
    ) -> None:
        """Send a signed transaction via ``jsonapi/sendtx``."""
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

        ``tx_types`` and ``tx_infos`` are wire-encoded as JSON-encoded
        string arrays (the form produced by the signer helpers).
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
                for channel in list(self._subscriptions):
                    await self._send_subscribe(channel)
                async for raw in ws:
                    if isinstance(raw, bytes):
                        logger.debug("Ignoring binary WebSocket frame")
                        continue
                    await self._dispatch(json.loads(raw))
            finally:
                self.ws = None
                self._send_lock = None

    async def _send_subscribe(self, channel: str) -> None:
        sub = self._subscriptions.get(channel)
        if sub is None:
            return
        payload: Dict[str, Any] = {"type": "subscribe", "channel": channel}
        token = sub.auth if sub.auth is not None else self._default_auth(channel)
        if token is not None:
            payload["auth"] = token
        await self.send_json(payload)

    def _default_auth(self, channel: str) -> Optional[str]:
        if channel.startswith(_AUTH_REQUIRED_PREFIXES):
            return self.auth
        return None

    def _spawn(self, coro: Coroutine[Any, Any, None]) -> None:
        """Schedule a coroutine on the running event loop, if any.

        Used so the sync :meth:`subscribe` / :meth:`unsubscribe` methods can
        also drive runtime subscribe/unsubscribe frames when the caller is
        inside an async context.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        loop.create_task(coro)

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
        if message_type.startswith("jsonapi/"):
            await self._call(self.on_tx_response, message)
            return
        if message_type == "connected" or not message_type.startswith(
            ("subscribed/", "update/")
        ):
            await self._call(self.on_message, message)
            return

        channel_raw = message.get("channel")
        if not isinstance(channel_raw, str):
            await self._call(self.on_message, message)
            return
        channel = _canonical_channel(channel_raw)

        if channel.startswith("order_book/"):
            self._update_order_book_state(channel, message)

        sub = self._subscriptions.get(channel)
        if sub is None:
            await self._call(self.on_message, message)
            return
        await self._call(sub.on_update, message)

    def _update_order_book_state(
        self, channel: str, message: Dict[str, Any]
    ) -> None:
        try:
            market_id = int(channel.split("/", 1)[1])
        except (IndexError, ValueError):
            return
        order_book = message.get("order_book") or {}
        if message.get("type") == "subscribed/order_book":
            self.order_book_states[market_id] = {
                "asks": list(order_book.get("asks") or []),
                "bids": list(order_book.get("bids") or []),
            }
            return
        state = self.order_book_states.setdefault(
            market_id, {"asks": [], "bids": []}
        )
        _apply_order_book_diff(order_book.get("asks") or [], state["asks"])
        _apply_order_book_diff(order_book.get("bids") or [], state["bids"])

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


def _canonical_channel(channel: str) -> str:
    """Normalize a channel string.

    Server-emitted channels use ``:`` as the separator (e.g.
    ``"order_book:0"``); subscribe requests in the docs use ``/`` (e.g.
    ``"order_book/0"``). The client stores and matches channels using
    ``/`` everywhere so users only have to remember one form.
    """
    return channel.replace(":", "/")


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

    Entries with size ``0`` remove the corresponding price level. The
    resulting list is not guaranteed to be sorted by price; consumers
    that need a sorted book should sort after each update.
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
