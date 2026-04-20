from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, IntEnum
from typing import Dict, List, Optional

_FEE_TICK = 1_000_000


class AccountTier(Enum):
    """Publicly documented account tiers with associated fee schedules.

    Each value is ``(taker_fee, maker_fee)`` expressed as fractions
    (i.e. ``280 / 1_000_000 == 0.000280 == 0.028 %``).

    Source: https://docs.lighter.xyz/trading/trading-fees
    """

    STANDARD = (0.0, 0.0)
    PREMIUM = (280 / _FEE_TICK, 40 / _FEE_TICK)
    PREMIUM_1 = (273 / _FEE_TICK, 39 / _FEE_TICK)
    PREMIUM_2 = (266 / _FEE_TICK, 38 / _FEE_TICK)
    PREMIUM_3 = (252 / _FEE_TICK, 36 / _FEE_TICK)
    PREMIUM_4 = (238 / _FEE_TICK, 34 / _FEE_TICK)
    PREMIUM_5 = (224 / _FEE_TICK, 32 / _FEE_TICK)
    PREMIUM_6 = (210 / _FEE_TICK, 30 / _FEE_TICK)
    PREMIUM_7 = (196 / _FEE_TICK, 28 / _FEE_TICK)

    @property
    def taker_fee(self) -> float:
        return self.value[0]

    @property
    def maker_fee(self) -> float:
        return self.value[1]


class PaperOrderType(IntEnum):
    MARKET = 0
    IOC = 1


class PaperOrderSide(IntEnum):
    BUY = 0
    SELL = 1


class PaperHealthStatus(IntEnum):
    HEALTHY = 0
    PRE_LIQUIDATION = 1
    # Values 2 (PARTIAL_LIQUIDATION) and 3 (FULL_LIQUIDATION) are reserved:
    # in real Lighter, accounts pass through TAV < MMR and TAV < COMR states,
    # but the paper sim collapses them. Liquidation runs atomically with every
    # mark update, so any position whose mark crosses liquidation_price is wiped
    # in the same tick.    
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
    # Sticky for the lifetime of the PaperClient session: set to True the first
    # time a paper liquidation fires and never cleared (no deposit/reset API).
    # Reads as "this session has experienced at least one liquidation", not
    # "currently liquidating". Recreate the PaperClient to reset.
    has_been_liquidated: bool = False


@dataclass
class PaperAccount:
    initial_collateral: float
    collateral: float
    positions: Dict[int, PaperPosition] = field(default_factory=dict)
    trades: List[PaperTrade] = field(default_factory=list)
    has_been_liquidated: bool = False


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


MarkPriceMap = Dict[int, float]
MarketConfigMap = Dict[int, MarketConfig]
