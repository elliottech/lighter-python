"""Typed envelopes for Lighter WebSocket messages.

Each server message ``type`` documented at
https://apidocs.lighter.xyz/docs/websocket-reference maps to a pydantic
envelope model below. All envelopes use ``extra="allow"`` and Optional
fields so that:

* New fields the server may add later do not raise validation errors
  (they end up in ``model_extra``).
* Missing fields show up as ``None`` instead of breaking parsing.

The envelopes are intentionally schema-loose. They give you completion
and a stable shape to write code against without coupling tightly to the
exact field set documented at any one point in time. If you need strict
validation, set ``model_config = ConfigDict(extra="forbid")`` on a
subclass.

Typical usage::

    from lighter import WsClient, ws_messages

    def on_book(message: ws_messages.WSOrderBookUpdate) -> None:
        for level in (message.order_book or {}).get("asks", []):
            ...

    client = WsClient()
    client.subscribe("order_book/0", on_update=on_book, parse=True)
    client.run()

Or standalone::

    parsed = ws_messages.parse_ws_message(raw_dict)
"""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Type, Union

from pydantic import BaseModel, ConfigDict


class WSEnvelope(BaseModel):
    """Base envelope for all Lighter WebSocket messages.

    Accepts unknown fields (forward compatible) and treats every
    channel-specific field as Optional so partial / new payloads parse
    without raising.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: str
    channel: Optional[str] = None


class WSConnected(WSEnvelope):
    """Server welcome message sent once per connection."""


class WSError(WSEnvelope):
    """Server-emitted error message."""

    message: Optional[str] = None
    code: Optional[int] = None


# ---------------------------------------------------------------------
# Public market data
# ---------------------------------------------------------------------


class WSOrderBookUpdate(WSEnvelope):
    """``subscribed/order_book`` snapshot or ``update/order_book`` diff."""

    order_book: Optional[Dict[str, Any]] = None


class WSTickerUpdate(WSEnvelope):
    ticker: Optional[Dict[str, Any]] = None


class WSMarketStatsUpdate(WSEnvelope):
    market_stats: Optional[Dict[str, Any]] = None


class WSSpotMarketStatsUpdate(WSEnvelope):
    market_stats: Optional[Dict[str, Any]] = None


class WSTradeUpdate(WSEnvelope):
    trades: Optional[List[Dict[str, Any]]] = None


class WSCandleUpdate(WSEnvelope):
    candle: Optional[Dict[str, Any]] = None
    resolution: Optional[str] = None


class WSHeightUpdate(WSEnvelope):
    height: Optional[int] = None


# ---------------------------------------------------------------------
# Account-scoped streams
# ---------------------------------------------------------------------


class WSAccountAllUpdate(WSEnvelope):
    """Combined account snapshot / diff from ``account_all/*``."""

    account_id: Optional[int] = None
    orders: Optional[List[Dict[str, Any]]] = None
    positions: Optional[List[Dict[str, Any]]] = None
    trades: Optional[List[Dict[str, Any]]] = None
    funding_histories: Optional[List[Dict[str, Any]]] = None
    funding_rates: Optional[List[Dict[str, Any]]] = None
    shares: Optional[List[Dict[str, Any]]] = None


class WSAccountMarketUpdate(WSEnvelope):
    account_id: Optional[int] = None
    market_id: Optional[int] = None
    orders: Optional[List[Dict[str, Any]]] = None
    positions: Optional[List[Dict[str, Any]]] = None
    trades: Optional[List[Dict[str, Any]]] = None


class WSAccountAllOrdersUpdate(WSEnvelope):
    account_id: Optional[int] = None
    orders: Optional[List[Dict[str, Any]]] = None


class WSAccountOrdersUpdate(WSEnvelope):
    account_id: Optional[int] = None
    market_id: Optional[int] = None
    orders: Optional[List[Dict[str, Any]]] = None


class WSAccountAllTradesUpdate(WSEnvelope):
    account_id: Optional[int] = None
    trades: Optional[List[Dict[str, Any]]] = None


class WSAccountAllPositionsUpdate(WSEnvelope):
    account_id: Optional[int] = None
    positions: Optional[List[Dict[str, Any]]] = None


class WSAccountAllAssetsUpdate(WSEnvelope):
    account_id: Optional[int] = None
    assets: Optional[Dict[str, Dict[str, Any]]] = None


class WSAccountSpotAvgEntryPricesUpdate(WSEnvelope):
    account_id: Optional[int] = None
    avg_entry_prices: Optional[Dict[str, Any]] = None


class WSAccountTxUpdate(WSEnvelope):
    account_id: Optional[int] = None
    txs: Optional[List[Dict[str, Any]]] = None


class WSUserStatsUpdate(WSEnvelope):
    account_id: Optional[int] = None
    stats: Optional[Dict[str, Any]] = None


class WSNotificationUpdate(WSEnvelope):
    account_id: Optional[int] = None
    notifications: Optional[List[Dict[str, Any]]] = None


class WSPoolDataUpdate(WSEnvelope):
    account_id: Optional[int] = None


class WSPoolInfoUpdate(WSEnvelope):
    account_id: Optional[int] = None


# ---------------------------------------------------------------------
# Transaction submission responses
# ---------------------------------------------------------------------


class WSTxResponse(WSEnvelope):
    """Response envelope for ``jsonapi/sendtx`` and ``jsonapi/sendtxbatch``."""

    id: Optional[str] = None
    code: Optional[int] = None
    message: Optional[str] = None
    tx_hash: Optional[str] = None
    tx_hashes: Optional[List[str]] = None
    error: Optional[Any] = None


# ---------------------------------------------------------------------
# Registry & dispatch helper
# ---------------------------------------------------------------------


_TYPE_MAP: Dict[str, Type[WSEnvelope]] = {
    "connected": WSConnected,
    "error": WSError,
    # public market data
    "subscribed/order_book": WSOrderBookUpdate,
    "update/order_book": WSOrderBookUpdate,
    "subscribed/ticker": WSTickerUpdate,
    "update/ticker": WSTickerUpdate,
    "subscribed/market_stats": WSMarketStatsUpdate,
    "update/market_stats": WSMarketStatsUpdate,
    "subscribed/spot_market_stats": WSSpotMarketStatsUpdate,
    "update/spot_market_stats": WSSpotMarketStatsUpdate,
    "subscribed/trade": WSTradeUpdate,
    "update/trade": WSTradeUpdate,
    "subscribed/candle": WSCandleUpdate,
    "update/candle": WSCandleUpdate,
    "subscribed/height": WSHeightUpdate,
    "update/height": WSHeightUpdate,
    # account-scoped
    "subscribed/account_all": WSAccountAllUpdate,
    "update/account_all": WSAccountAllUpdate,
    "subscribed/account_market": WSAccountMarketUpdate,
    "update/account_market": WSAccountMarketUpdate,
    "subscribed/account_all_orders": WSAccountAllOrdersUpdate,
    "update/account_all_orders": WSAccountAllOrdersUpdate,
    "subscribed/account_orders": WSAccountOrdersUpdate,
    "update/account_orders": WSAccountOrdersUpdate,
    "subscribed/account_all_trades": WSAccountAllTradesUpdate,
    "update/account_all_trades": WSAccountAllTradesUpdate,
    "subscribed/account_all_positions": WSAccountAllPositionsUpdate,
    "update/account_all_positions": WSAccountAllPositionsUpdate,
    "subscribed/account_all_assets": WSAccountAllAssetsUpdate,
    "update/account_all_assets": WSAccountAllAssetsUpdate,
    "subscribed/account_spot_avg_entry_prices": (
        WSAccountSpotAvgEntryPricesUpdate
    ),
    "update/account_spot_avg_entry_prices": WSAccountSpotAvgEntryPricesUpdate,
    "subscribed/account_tx": WSAccountTxUpdate,
    "update/account_tx": WSAccountTxUpdate,
    "subscribed/user_stats": WSUserStatsUpdate,
    "update/user_stats": WSUserStatsUpdate,
    "subscribed/notification": WSNotificationUpdate,
    "update/notification": WSNotificationUpdate,
    "subscribed/pool_data": WSPoolDataUpdate,
    "update/pool_data": WSPoolDataUpdate,
    "subscribed/pool_info": WSPoolInfoUpdate,
    "update/pool_info": WSPoolInfoUpdate,
    # transaction submission responses
    "jsonapi/sendtx": WSTxResponse,
    "jsonapi/sendtxbatch": WSTxResponse,
}


def envelope_for(message_type: str) -> Optional[Type[WSEnvelope]]:
    """Return the envelope class registered for ``message_type``, or ``None``."""
    return _TYPE_MAP.get(message_type)


def parse_ws_message(
    message: Mapping[str, Any],
) -> Union[WSEnvelope, Mapping[str, Any]]:
    """Parse a raw WS message into a typed envelope.

    Returns the input ``message`` unchanged if no envelope is registered
    for the message ``type`` (e.g. an unknown channel kind), so callers
    can still rely on a dict-shaped fallback.
    """
    msg_type = message.get("type")
    if not isinstance(msg_type, str):
        return message
    cls = _TYPE_MAP.get(msg_type)
    if cls is None:
        return message
    return cls.model_validate(message)


__all__ = [
    "WSEnvelope",
    "WSConnected",
    "WSError",
    "WSOrderBookUpdate",
    "WSTickerUpdate",
    "WSMarketStatsUpdate",
    "WSSpotMarketStatsUpdate",
    "WSTradeUpdate",
    "WSCandleUpdate",
    "WSHeightUpdate",
    "WSAccountAllUpdate",
    "WSAccountMarketUpdate",
    "WSAccountAllOrdersUpdate",
    "WSAccountOrdersUpdate",
    "WSAccountAllTradesUpdate",
    "WSAccountAllPositionsUpdate",
    "WSAccountAllAssetsUpdate",
    "WSAccountSpotAvgEntryPricesUpdate",
    "WSAccountTxUpdate",
    "WSUserStatsUpdate",
    "WSNotificationUpdate",
    "WSPoolDataUpdate",
    "WSPoolInfoUpdate",
    "WSTxResponse",
    "envelope_for",
    "parse_ws_message",
]
