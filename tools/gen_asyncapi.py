"""Generate asyncapi.json for the Lighter WebSocket API.

This script is a one-shot generator — only the produced ``asyncapi.json``
is checked into the repo. The script lives outside the repo and is kept
in this file purely so the spec can be reproduced or extended later.

The structure follows AsyncAPI 3.0 (https://www.asyncapi.com/docs/reference/specification/v3.0.0).
"""

from __future__ import annotations

import json
from typing import Any, Dict, List


# ---------------------------------------------------------------------
# Reused data schemas (from the "Types" section of the docs)
# ---------------------------------------------------------------------

# All shared schemas keep ``additionalProperties: true`` so that
# server-side field additions don't require a spec bump to keep clients
# parsing successfully. Channel-specific fields are optional for the
# same reason.

SHARED_SCHEMAS: Dict[str, Dict[str, Any]] = {
    "Transaction": {
        "type": "object",
        "additionalProperties": True,
        "description": "Transaction as emitted on the `account_tx` channel.",
        "properties": {
            "hash": {"type": "string"},
            "type": {"type": "integer"},
            "info": {"type": "string", "description": "JSON object encoded as string; shape depends on tx type."},
            "event_info": {"type": "string", "description": "JSON object encoded as string; shape depends on tx type."},
            "status": {"type": "integer"},
            "transaction_index": {"type": "integer"},
            "l1_address": {"type": "string"},
            "account_index": {"type": "integer"},
            "nonce": {"type": "integer"},
            "expire_at": {"type": "integer"},
            "block_height": {"type": "integer"},
            "queued_at": {"type": "integer"},
            "executed_at": {"type": "integer"},
            "sequence_index": {"type": "integer"},
            "parent_hash": {"type": "string"},
            "api_key_index": {"type": "integer"},
            "transaction_time": {"type": "integer"},
        },
    },
    "Order": {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "order_index": {"type": "integer"},
            "client_order_index": {"type": "integer"},
            "order_id": {"type": "string"},
            "client_order_id": {"type": "string"},
            "market_index": {"type": "integer"},
            "owner_account_index": {"type": "integer"},
            "initial_base_amount": {"type": "string"},
            "price": {"type": "string"},
            "nonce": {"type": "integer"},
            "remaining_base_amount": {"type": "string"},
            "is_ask": {"type": "boolean"},
            "base_size": {"type": "integer"},
            "base_price": {"type": "integer"},
            "filled_base_amount": {"type": "string"},
            "filled_quote_amount": {"type": "string"},
            "side": {"type": "string"},
            "type": {
                "type": "string",
                "enum": [
                    "limit",
                    "market",
                    "stop-loss",
                    "stop-loss-limit",
                    "take-profit",
                    "take-profit-limit",
                    "twap",
                    "twap-sub",
                    "liquidation",
                ],
            },
            "time_in_force": {
                "type": "string",
                "enum": [
                    "good-till-time",
                    "immediate-or-cancel",
                    "post-only",
                    "Unknown",
                ],
            },
            "reduce_only": {"type": "boolean"},
            "trigger_price": {"type": "string"},
            "order_expiry": {"type": "integer"},
            "status": {"type": "string"},
            "trigger_status": {"type": "string"},
            "trigger_time": {"type": "integer"},
            "parent_order_index": {"type": "integer"},
            "parent_order_id": {"type": "string"},
            "to_trigger_order_id_0": {"type": "string"},
            "to_trigger_order_id_1": {"type": "string"},
            "to_cancel_order_id_0": {"type": "string"},
            "integrator_fee_collector_index": {"type": "string"},
            "integrator_taker_fee": {"type": "string"},
            "integrator_maker_fee": {"type": "string"},
            "block_height": {"type": "integer"},
        },
    },
    "Trade": {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "trade_id": {"type": "integer"},
            "market_id": {"type": "integer"},
            "size": {"type": "string"},
            "price": {"type": "string"},
            "usd_amount": {"type": "string"},
            "ask_id": {"type": "integer"},
            "ask_account_id": {"type": "integer"},
            "bid_id": {"type": "integer"},
            "bid_account_id": {"type": "integer"},
            "is_maker_ask": {"type": "boolean"},
            "block_height": {"type": "integer"},
            "timestamp": {"type": "integer"},
            "type": {"type": "string"},
        },
    },
    "Position": {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "market_id": {"type": "integer"},
            "sign": {"type": "integer"},
            "position": {"type": "string"},
            "avg_entry_price": {"type": "string"},
            "position_value": {"type": "string"},
            "unrealized_pnl": {"type": "string"},
            "realized_pnl": {"type": "string"},
            "margin_mode": {"type": "integer"},
            "allocated_margin": {"type": "string"},
            "liquidation_price": {"type": "string"},
        },
    },
    "PoolShares": {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "pool_account_index": {"type": "integer"},
            "owner_account_index": {"type": "integer"},
            "shares_amount": {"type": "string"},
            "entry_usdc_amount": {"type": "string"},
        },
    },
    "Asset": {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "symbol": {"type": "string"},
            "asset_id": {"type": "integer"},
            "balance": {"type": "string"},
            "locked_balance": {"type": "string"},
        },
    },
    "PositionFunding": {
        "type": "object",
        "additionalProperties": True,
        "properties": {
            "timestamp": {"type": "integer"},
            "market_id": {"type": "integer"},
            "funding_id": {"type": "integer"},
            "change": {"type": "string"},
            "rate": {"type": "string"},
            "position_size": {"type": "string"},
            "position_side": {"type": "string", "enum": ["long", "short"]},
            "discount": {"type": "string"},
        },
    },
}


# ---------------------------------------------------------------------
# Channels.
#
# Each entry: id, address (with {param} placeholders), parameters,
# whether subscribe requires auth, and the message-payload extras
# (fields beyond the envelope's `type` + `channel`).
# ---------------------------------------------------------------------


def envelope_payload(extras: Dict[str, Any]) -> Dict[str, Any]:
    """Build the JSON Schema for a server message payload.

    Every message carries ``type`` and ``channel``; everything else is
    channel-specific and optional. ``additionalProperties: true`` is
    deliberate (see the forward-compat policy in ws_messages.py).
    """
    return {
        "type": "object",
        "additionalProperties": True,
        "required": ["type"],
        "properties": {
            "type": {"type": "string"},
            "channel": {"type": "string"},
            "timestamp": {"type": "integer"},
            **extras,
        },
    }


CHANNELS: List[Dict[str, Any]] = [
    # ----- public market data -----
    {
        "id": "order_book",
        "address": "order_book/{market_id}",
        "parameters": {"market_id": {"description": "Market index."}},
        "auth_required": False,
        "title": "Order Book",
        "description": "Order book snapshots and diffs for a given market. Snapshots ship on subscribe; subsequent messages are price-level diffs.",
        "payload_extras": {
            "order_book": {
                "type": "object",
                "additionalProperties": True,
                "properties": {
                    "asks": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
                    "bids": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
                    "offset": {"type": "integer"},
                },
            },
        },
    },
    {
        "id": "ticker",
        "address": "ticker/{market_id}",
        "parameters": {"market_id": {"description": "Market index."}},
        "auth_required": False,
        "title": "Best Bid and Offer (BBO)",
        "description": "Best bid/offer updates for a given market.",
        "payload_extras": {
            "ticker": {"type": "object", "additionalProperties": True},
        },
    },
    {
        "id": "market_stats",
        "address": "market_stats/{market_id}",
        "parameters": {
            "market_id": {
                "description": "Market index, or the literal string `all` to receive stats for every market.",
            },
        },
        "auth_required": False,
        "title": "Market Stats",
        "description": "Per-market rolling stats (volume, price change, etc.). Pass `all` as the market id to receive every market on one subscription.",
        "payload_extras": {
            "market_stats": {"type": "object", "additionalProperties": True},
        },
    },
    {
        "id": "spot_market_stats",
        "address": "spot_market_stats/{market_id}",
        "parameters": {
            "market_id": {
                "description": "Spot market index, or the literal string `all`.",
            },
        },
        "auth_required": False,
        "title": "Spot Market Stats",
        "description": "Per-spot-market rolling stats. Pass `all` to receive every spot market on one subscription.",
        "payload_extras": {
            "spot_market_stats": {"type": "object", "additionalProperties": True},
        },
    },
    {
        "id": "trade",
        "address": "trade/{market_id}",
        "parameters": {"market_id": {"description": "Market index."}},
        "auth_required": False,
        "title": "Trade",
        "description": "Public trade stream for a given market.",
        "payload_extras": {
            "trades": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/Trade"},
            },
        },
    },
    {
        "id": "candle",
        "address": "candle/{market_id}/{resolution}",
        "parameters": {
            "market_id": {"description": "Market index."},
            "resolution": {
                "description": "Candle resolution, e.g. `1m`, `5m`, `1h`, `1d`.",
            },
        },
        "auth_required": False,
        "title": "Candlesticks",
        "description": "Candlestick stream for a (market, resolution) pair.",
        "payload_extras": {
            "candle": {"type": "object", "additionalProperties": True},
            "resolution": {"type": "string"},
        },
    },
    {
        "id": "height",
        "address": "height",
        "parameters": {},
        "auth_required": False,
        "title": "Height",
        "description": "Latest L2 block height.",
        "payload_extras": {
            "height": {"type": "integer"},
        },
    },
    # ----- account-scoped streams -----
    {
        "id": "account_all",
        "address": "account_all/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        # The docs subscribe example does not show an `auth` field for
        # this channel. Marked unauthenticated in the spec for parity;
        # see the README note next to AUTH_REQUIRED_PREFIXES in
        # ws_client.py — the auth-required list is documented to match
        # the docs page exactly.
        "auth_required": False,
        "title": "Account All",
        "description": "Combined account stream: orders, positions, trades, funding histories/rates, and pool shares.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "orders": {"type": "array", "items": {"$ref": "#/components/schemas/Order"}},
            "positions": {"type": "array", "items": {"$ref": "#/components/schemas/Position"}},
            "trades": {"type": "array", "items": {"$ref": "#/components/schemas/Trade"}},
            "funding_histories": {"type": "array", "items": {"$ref": "#/components/schemas/PositionFunding"}},
            "funding_rates": {"type": "array", "items": {"type": "object", "additionalProperties": True}},
            "shares": {"type": "array", "items": {"$ref": "#/components/schemas/PoolShares"}},
        },
    },
    {
        "id": "account_market",
        "address": "account_market/{market_id}/{account_id}",
        "parameters": {
            "market_id": {"description": "Market index."},
            "account_id": {"description": "Account index."},
        },
        "auth_required": True,
        "title": "Account Market",
        "description": "Per-market view of a specific account (orders, positions, trades restricted to one market).",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "market_id": {"type": "integer"},
            "orders": {"type": "array", "items": {"$ref": "#/components/schemas/Order"}},
            "positions": {"type": "array", "items": {"$ref": "#/components/schemas/Position"}},
            "trades": {"type": "array", "items": {"$ref": "#/components/schemas/Trade"}},
        },
    },
    {
        "id": "user_stats",
        "address": "user_stats/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": False,
        "title": "Account Stats",
        "description": "Aggregate stats for an account (collateral, portfolio value, etc.).",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "stats": {"type": "object", "additionalProperties": True},
        },
    },
    {
        "id": "account_tx",
        "address": "account_tx/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": True,
        "title": "Account Tx",
        "description": "Transaction history for a specific account.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "txs": {
                "type": "array",
                "items": {"$ref": "#/components/schemas/Transaction"},
            },
        },
    },
    {
        "id": "account_all_orders",
        "address": "account_all_orders/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": True,
        "title": "Account All Orders",
        "description": "All orders across markets for an account.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "orders": {"type": "array", "items": {"$ref": "#/components/schemas/Order"}},
        },
    },
    {
        "id": "account_orders",
        "address": "account_orders/{market_id}/{account_id}",
        "parameters": {
            "market_id": {"description": "Market index."},
            "account_id": {"description": "Account index."},
        },
        "auth_required": True,
        "title": "Account Orders",
        "description": "Orders for an account scoped to a single market.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "market_id": {"type": "integer"},
            "orders": {"type": "array", "items": {"$ref": "#/components/schemas/Order"}},
        },
    },
    {
        "id": "account_all_trades",
        "address": "account_all_trades/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": False,
        "title": "Account All Trades",
        "description": "All trades for an account across markets. Snapshot keys trades by market index; updates may emit a flat list.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "trades": {
                "oneOf": [
                    {"type": "array", "items": {"$ref": "#/components/schemas/Trade"}},
                    {
                        "type": "object",
                        "additionalProperties": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Trade"},
                        },
                    },
                ],
            },
            "total_volume": {"type": "number"},
            "monthly_volume": {"type": "number"},
        },
    },
    {
        "id": "account_all_positions",
        "address": "account_all_positions/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": False,
        "title": "Account All Positions",
        "description": "All positions for an account, keyed by market index.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "positions": {
                "type": "object",
                "additionalProperties": {"$ref": "#/components/schemas/Position"},
            },
        },
    },
    {
        "id": "account_all_assets",
        "address": "account_all_assets/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": True,
        "title": "Account All Assets",
        "description": "Per-asset balances for all spot markets for a specific account. `balance` is in coin terms, not USDC.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "assets": {
                "type": "object",
                "additionalProperties": {"$ref": "#/components/schemas/Asset"},
            },
        },
    },
    {
        "id": "account_spot_avg_entry_prices",
        "address": "account_spot_avg_entry_prices/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": True,
        "title": "Average Entry Prices",
        "description": "Spot avg-entry-price stream. Each event accounts as a buy/sell at the index price; `last_trade_id` confirms the validity horizon.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "avg_entry_prices": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "additionalProperties": True,
                    "properties": {
                        "asset_id": {"type": "integer"},
                        "avg_entry_price": {"type": "string"},
                        "asset_size": {"type": "string"},
                        "last_trade_id": {"type": "integer"},
                    },
                },
            },
        },
    },
    {
        "id": "notification",
        "address": "notification/{account_id}",
        "parameters": {"account_id": {"description": "Account index."}},
        "auth_required": True,
        "title": "Notification",
        "description": "Per-account notification stream.",
        "payload_extras": {
            "account_id": {"type": "integer"},
            "notifications": {
                "type": "array",
                "items": {"type": "object", "additionalProperties": True},
            },
        },
    },
    {
        "id": "pool_data",
        "address": "pool_data/{account_id}",
        "parameters": {"account_id": {"description": "Pool account index."}},
        "auth_required": True,
        "title": "Pool Data",
        "description": "Live data for a public pool account.",
        "payload_extras": {
            "account_id": {"type": "integer"},
        },
    },
    {
        "id": "pool_info",
        "address": "pool_info/{account_id}",
        "parameters": {"account_id": {"description": "Pool account index."}},
        "auth_required": True,
        "title": "Pool Info",
        "description": "Public pool metadata.",
        "payload_extras": {
            "account_id": {"type": "integer"},
        },
    },
]


# ---------------------------------------------------------------------
# Build the document
# ---------------------------------------------------------------------


def build_message_components() -> Dict[str, Dict[str, Any]]:
    messages: Dict[str, Dict[str, Any]] = {}
    # Per-channel server messages.
    for ch in CHANNELS:
        camel = "".join(p.title() for p in ch["id"].split("_"))
        payload_schema = envelope_payload(ch["payload_extras"])
        subscribed_type = f"subscribed/{ch['id']}"
        update_type = f"update/{ch['id']}"
        messages[f"{camel}Subscribed"] = {
            "name": f"{camel}Subscribed",
            "title": f"{ch['title']} snapshot",
            "summary": f"Initial snapshot delivered after a successful `subscribe` to `{ch['address']}`.",
            "x-message-type": subscribed_type,
            "contentType": "application/json",
            "payload": payload_schema,
        }
        messages[f"{camel}Update"] = {
            "name": f"{camel}Update",
            "title": f"{ch['title']} update",
            "summary": f"Live update for an existing subscription to `{ch['address']}`.",
            "x-message-type": update_type,
            "contentType": "application/json",
            "payload": payload_schema,
        }

    # Global / control-plane messages.
    messages["Connected"] = {
        "name": "Connected",
        "title": "Connection welcome",
        "summary": "Sent once when the WebSocket connection is established.",
        "x-message-type": "connected",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type"],
            "properties": {"type": {"const": "connected"}},
        },
    }
    messages["ServerError"] = {
        "name": "ServerError",
        "title": "Server error",
        "summary": "Server-emitted error frame.",
        "x-message-type": "error",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type"],
            "properties": {
                "type": {"const": "error"},
                "message": {"type": "string"},
                "code": {"type": "integer"},
            },
        },
    }
    messages["Pong"] = {
        "name": "Pong",
        "title": "Application-level pong",
        "summary": "Reply to a client-sent `ping` frame.",
        "x-message-type": "pong",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type"],
            "properties": {"type": {"const": "pong"}},
        },
    }
    messages["TxResponse"] = {
        "name": "TxResponse",
        "title": "Transaction submission response",
        "summary": "Reply to `jsonapi/sendtx` or `jsonapi/sendtxbatch`.",
        "x-message-type": "jsonapi/sendtx",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type"],
            "properties": {
                "type": {"type": "string"},
                "id": {"type": "string"},
                "code": {"type": "integer"},
                "message": {"type": "string"},
                "tx_hash": {"type": "string"},
                "tx_hashes": {"type": "array", "items": {"type": "string"}},
                "error": {},
            },
        },
    }

    # Client → server messages.
    messages["SubscribeRequest"] = {
        "name": "SubscribeRequest",
        "title": "Subscribe",
        "summary": "Open a subscription on a channel.",
        "x-message-type": "subscribe",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type", "channel"],
            "properties": {
                "type": {"const": "subscribe"},
                "channel": {
                    "type": "string",
                    "description": "Channel address. Use `/` as the path separator (e.g. `order_book/0`).",
                },
                "auth": {
                    "type": "string",
                    "description": "Bearer token. Required for the channels listed under `securitySchemes.bearerToken`.",
                },
            },
        },
    }
    messages["UnsubscribeRequest"] = {
        "name": "UnsubscribeRequest",
        "title": "Unsubscribe",
        "summary": "Cancel an existing subscription.",
        "x-message-type": "unsubscribe",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type", "channel"],
            "properties": {
                "type": {"const": "unsubscribe"},
                "channel": {"type": "string"},
            },
        },
    }
    messages["Ping"] = {
        "name": "Ping",
        "title": "Application-level ping",
        "summary": "Heartbeat frame. The server replies with a `Pong`. Either WebSocket-level ping frames or this application-level frame satisfy the 2-minute idle requirement.",
        "x-message-type": "ping",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type"],
            "properties": {"type": {"const": "ping"}},
        },
    }
    messages["SendTx"] = {
        "name": "SendTx",
        "title": "Send transaction",
        "summary": "Submit a single signed transaction over the socket.",
        "x-message-type": "jsonapi/sendtx",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type", "data"],
            "properties": {
                "type": {"const": "jsonapi/sendtx"},
                "data": {
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["tx_type", "tx_info"],
                    "properties": {
                        "tx_type": {"type": "integer"},
                        "tx_info": {
                            "description": "Signed payload produced by SignerClient. Usually a JSON-encoded string.",
                        },
                    },
                },
            },
        },
    }
    messages["SendTxBatch"] = {
        "name": "SendTxBatch",
        "title": "Send transaction batch",
        "summary": "Submit up to 15 signed transactions in one message. `tx_infos` is a JSON-encoded list of JSON-encoded `tx_info` strings (double-encoded).",
        "x-message-type": "jsonapi/sendtxbatch",
        "contentType": "application/json",
        "payload": {
            "type": "object",
            "additionalProperties": True,
            "required": ["type", "data"],
            "properties": {
                "type": {"const": "jsonapi/sendtxbatch"},
                "data": {
                    "type": "object",
                    "additionalProperties": True,
                    "required": ["tx_types", "tx_infos"],
                    "properties": {
                        "tx_types": {
                            "type": "string",
                            "description": "JSON-encoded list of integer tx types, e.g. `\"[14,14]\"`.",
                        },
                        "tx_infos": {
                            "type": "string",
                            "description": "JSON-encoded list of JSON-encoded tx_info strings.",
                        },
                    },
                },
            },
        },
    }

    return messages


def build_channels() -> Dict[str, Dict[str, Any]]:
    channels: Dict[str, Dict[str, Any]] = {}
    for ch in CHANNELS:
        camel = "".join(p.title() for p in ch["id"].split("_"))
        params = {
            name: {"description": spec["description"]}
            for name, spec in ch["parameters"].items()
        }
        ch_doc: Dict[str, Any] = {
            "address": ch["address"],
            "title": ch["title"],
            "description": ch["description"],
            "messages": {
                f"{camel}Subscribed": {"$ref": f"#/components/messages/{camel}Subscribed"},
                f"{camel}Update": {"$ref": f"#/components/messages/{camel}Update"},
            },
        }
        if params:
            ch_doc["parameters"] = params
        channels[ch["id"]] = ch_doc

    # Single control-plane channel for everything that isn't tied to a
    # subscription address (the WebSocket itself).
    channels["_control"] = {
        "address": "(connection)",
        "title": "Connection control plane",
        "description": "Frames not tied to a subscription address: client → server `subscribe`/`unsubscribe`/`ping`/`jsonapi/sendtx`/`jsonapi/sendtxbatch`, and server → client `connected`/`error`/`pong`/`jsonapi/*` responses.",
        "messages": {
            "SubscribeRequest": {"$ref": "#/components/messages/SubscribeRequest"},
            "UnsubscribeRequest": {"$ref": "#/components/messages/UnsubscribeRequest"},
            "Ping": {"$ref": "#/components/messages/Ping"},
            "SendTx": {"$ref": "#/components/messages/SendTx"},
            "SendTxBatch": {"$ref": "#/components/messages/SendTxBatch"},
            "Connected": {"$ref": "#/components/messages/Connected"},
            "ServerError": {"$ref": "#/components/messages/ServerError"},
            "Pong": {"$ref": "#/components/messages/Pong"},
            "TxResponse": {"$ref": "#/components/messages/TxResponse"},
        },
    }
    return channels


def build_operations() -> Dict[str, Dict[str, Any]]:
    operations: Dict[str, Dict[str, Any]] = {}
    for ch in CHANNELS:
        camel = "".join(p.title() for p in ch["id"].split("_"))
        sub_op: Dict[str, Any] = {
            "action": "send",
            "channel": {"$ref": f"#/channels/{ch['id']}"},
            "summary": f"Subscribe to `{ch['address']}`.",
            "messages": [{"$ref": "#/components/messages/SubscribeRequest"}],
        }
        if ch["auth_required"]:
            sub_op["security"] = [{"$ref": "#/components/securitySchemes/bearerToken"}]
        operations[f"subscribe_{ch['id']}"] = sub_op

        operations[f"receive_{ch['id']}"] = {
            "action": "receive",
            "channel": {"$ref": f"#/channels/{ch['id']}"},
            "summary": f"Receive snapshot + updates for `{ch['address']}`.",
            "messages": [
                {"$ref": f"#/channels/{ch['id']}/messages/{camel}Subscribed"},
                {"$ref": f"#/channels/{ch['id']}/messages/{camel}Update"},
            ],
        }

    # Control-plane operations.
    operations["unsubscribe"] = {
        "action": "send",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Cancel an existing subscription.",
        "messages": [{"$ref": "#/components/messages/UnsubscribeRequest"}],
    }
    operations["ping"] = {
        "action": "send",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Application-level heartbeat (server replies with `Pong`).",
        "messages": [{"$ref": "#/components/messages/Ping"}],
    }
    operations["send_tx"] = {
        "action": "send",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Submit a single signed transaction.",
        "messages": [{"$ref": "#/components/messages/SendTx"}],
    }
    operations["send_tx_batch"] = {
        "action": "send",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Submit up to 15 signed transactions in a single frame.",
        "messages": [{"$ref": "#/components/messages/SendTxBatch"}],
    }
    operations["receive_connected"] = {
        "action": "receive",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Connection welcome frame.",
        "messages": [{"$ref": "#/channels/_control/messages/Connected"}],
    }
    operations["receive_error"] = {
        "action": "receive",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Server error frame.",
        "messages": [{"$ref": "#/channels/_control/messages/ServerError"}],
    }
    operations["receive_pong"] = {
        "action": "receive",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Reply to a client `Ping`.",
        "messages": [{"$ref": "#/channels/_control/messages/Pong"}],
    }
    operations["receive_tx_response"] = {
        "action": "receive",
        "channel": {"$ref": "#/channels/_control"},
        "summary": "Reply to `jsonapi/sendtx` or `jsonapi/sendtxbatch` (success or error).",
        "messages": [{"$ref": "#/channels/_control/messages/TxResponse"}],
    }
    return operations


def build_document() -> Dict[str, Any]:
    return {
        "asyncapi": "3.0.0",
        "info": {
            "title": "Lighter WebSocket API",
            "version": "1.0.0",
            "description": (
                "Real-time market data, account state, and transaction submission "
                "for the zkLighter exchange. Hand-mirrored from "
                "https://apidocs.lighter.xyz/docs/websocket-reference. The schemas "
                "are intentionally permissive (`additionalProperties: true`, all "
                "channel-specific fields optional) so server-side additions do "
                "not invalidate generated clients."
            ),
            "contact": {
                "name": "Lighter API docs",
                "url": "https://apidocs.lighter.xyz/docs/websocket-reference",
            },
        },
        "defaultContentType": "application/json",
        "servers": {
            "mainnet": {
                "host": "mainnet.zklighter.elliot.ai",
                "pathname": "/stream",
                "protocol": "wss",
                "description": "Mainnet WebSocket gateway. Append `?readonly=true` to bypass IP region restrictions for read-only data.",
            },
            "testnet": {
                "host": "testnet.zklighter.elliot.ai",
                "pathname": "/stream",
                "protocol": "wss",
                "description": "Testnet WebSocket gateway.",
            },
        },
        "channels": build_channels(),
        "operations": build_operations(),
        "components": {
            "messages": build_message_components(),
            "schemas": SHARED_SCHEMAS,
            "securitySchemes": {
                "bearerToken": {
                    "type": "http",
                    "scheme": "bearer",
                    "description": (
                        "Per-channel auth token passed in the `auth` field of the `subscribe` "
                        "message. Required for channels whose subscribe operation lists this "
                        "scheme under `security`. See the `apikeys` REST endpoint for token "
                        "generation."
                    ),
                },
            },
        },
    }


if __name__ == "__main__":
    import sys

    out = build_document()
    json.dump(out, sys.stdout, indent=2, sort_keys=False)
    sys.stdout.write("\n")
