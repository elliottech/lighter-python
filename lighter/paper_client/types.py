from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import IntEnum
from typing import Dict, List, Optional


class PaperOrderType(IntEnum):
    MARKET = 0
    IOC = 1


class PaperOrderSide(IntEnum):
    BUY = 0
    SELL = 1


class PaperHealthStatus(IntEnum):
    HEALTHY = 0
    PRE_LIQUIDATION = 1
    PARTIAL_LIQUIDATION = 2
    FULL_LIQUIDATION = 3
    BANKRUPTCY = 4


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass(frozen=True)
class PaperOrderRequest:
    market_id: int
    side: PaperOrderSide
    base_amount: float
    price: float = 0
    order_type: PaperOrderType = PaperOrderType.MARKET


@dataclass(frozen=True)
class PaperFill:
    price: float
    size: float
    fee: float
    is_maker: bool = False


@dataclass(frozen=True)
class PaperOrderResult:
    order_type: PaperOrderType
    side: PaperOrderSide
    market_id: int
    fills: List[PaperFill]
    filled_size: float
    avg_price: float
    total_fee: float
    quote_amount: float
    unfilled: float
    timestamp: datetime
    liquidated: bool = False


@dataclass
class PaperPosition:
    market_id: int
    size: float = 0
    entry_quote: float = 0
    avg_entry_price: float = 0
    mark_price: float = 0
    unrealized_pnl: float = 0
    realized_pnl: float = 0
    liquidation_price: float = 0


@dataclass(frozen=True)
class PaperTrade:
    market_id: int
    side: PaperOrderSide
    size: float
    price: float
    fee: float
    realized_pnl: float
    is_liquidation: bool
    timestamp: datetime


@dataclass(frozen=True)
class PaperAccountHealth:
    status: PaperHealthStatus
    total_account_value: float
    initial_margin_requirement: float
    maintenance_margin_requirement: float
    margin_usage: float
    leverage: float


@dataclass
class PaperAccount:
    initial_collateral: float
    collateral: float
    positions: Dict[int, PaperPosition] = field(default_factory=dict)
    trades: List[PaperTrade] = field(default_factory=list)


@dataclass(frozen=True)
class MarketConfig:
    market_id: int
    symbol: str
    size_decimals: int
    price_decimals: int
    default_initial_margin_fraction: int
    min_initial_margin_fraction: int
    maintenance_margin_fraction: int
    closeout_margin_fraction: int
    taker_fee: float
    maker_fee: float
    min_base_amount: float
    min_quote_amount: float
    last_trade_price: float


PositionMap = Dict[int, PaperPosition]
MarkPriceMap = Dict[int, float]
MarketConfigMap = Dict[int, MarketConfig]
MaybePosition = Optional[PaperPosition]
