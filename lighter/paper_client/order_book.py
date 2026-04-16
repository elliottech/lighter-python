from dataclasses import dataclass, field
from typing import Any, Iterable, List, Mapping, Optional, Tuple, Union

from lighter.models.order_book_depth import OrderBookDepth
from lighter.models.order_book_orders import OrderBookOrders
from lighter.models.price_level import PriceLevel
from lighter.models.simple_order import SimpleOrder


OrderBookLevelLike = Union["OrderBookLevel", PriceLevel, SimpleOrder, Mapping[str, Any]]


@dataclass(frozen=True)
class OrderBookLevel:
    price: str
    size: str

    @classmethod
    def from_any(cls, level: OrderBookLevelLike) -> "OrderBookLevel":
        if isinstance(level, cls):
            return level

        if isinstance(level, PriceLevel):
            return cls(price=level.price, size=level.size)

        if isinstance(level, SimpleOrder):
            return cls(price=level.price, size=level.remaining_base_amount)

        if isinstance(level, Mapping):
            price = level.get("price")
            size = level.get("size", level.get("remaining_base_amount"))
            if price is None or size is None:
                raise ValueError("Order book levels must include price and size data.")
            return cls(price=str(price), size=str(size))

        raise TypeError(f"Unsupported order book level type: {type(level)!r}")

    @property
    def price_float(self) -> float:
        return float(self.price)

    @property
    def size_float(self) -> float:
        return float(self.size)

    def to_dict(self) -> Mapping[str, str]:
        return {"price": self.price, "size": self.size}


@dataclass
class InMemoryOrderBook:
    """Sorted in-memory order book built for ``PaperClient`` to simulate 
    taker fills against order book data. Keeps asks sorted ascending and 
    bids sorted descending so the best prices are always at index 0.  
    """

    asks: List[OrderBookLevel] = field(default_factory=list)
    bids: List[OrderBookLevel] = field(default_factory=list)
    offset: Optional[int] = None

    def __post_init__(self) -> None:
        self.asks = self._sorted_levels(self.asks, is_asks=True)
        self.bids = self._sorted_levels(self.bids, is_asks=False)

    def apply_snapshot(
        self,
        snapshot: Union[OrderBookOrders, OrderBookDepth, Mapping[str, Any]],
    ) -> None:
        asks, bids, offset = self._extract_book_data(snapshot)
        self.asks = self._sorted_levels(asks, is_asks=True)
        self.bids = self._sorted_levels(bids, is_asks=False)
        self.offset = offset

    def apply_delta(
        self, delta: Union[OrderBookDepth, Mapping[str, Any]]
    ) -> None:
        asks, bids, offset = self._extract_book_data(delta)
        self.asks = self._merge_levels(self.asks, asks, is_asks=True)
        self.bids = self._merge_levels(self.bids, bids, is_asks=False)
        self.offset = offset

    @property
    def best_ask(self) -> Optional[OrderBookLevel]:
        return self.asks[0] if self.asks else None

    @property
    def best_bid(self) -> Optional[OrderBookLevel]:
        return self.bids[0] if self.bids else None

    @property
    def mid_price(self) -> Optional[float]:
        if self.best_ask is None or self.best_bid is None:
            return None
        return (self.best_ask.price_float + self.best_bid.price_float) / 2

    def to_dict(self) -> Mapping[str, Any]:
        return {
            "asks": [level.to_dict() for level in self.asks],
            "bids": [level.to_dict() for level in self.bids],
            "offset": self.offset,
        }

    @staticmethod
    def _extract_book_data(
        payload: Union[OrderBookOrders, OrderBookDepth, Mapping[str, Any]]
    ) -> Tuple[Iterable[OrderBookLevelLike], Iterable[OrderBookLevelLike], Optional[int]]:
        if isinstance(payload, OrderBookOrders):
            return payload.asks, payload.bids, None

        if isinstance(payload, OrderBookDepth):
            return payload.asks, payload.bids, payload.offset

        if not isinstance(payload, Mapping):
            raise TypeError(f"Unsupported order book payload type: {type(payload)!r}")

        asks = payload.get("asks", [])
        bids = payload.get("bids", [])
        offset = payload.get("offset")
        return asks, bids, offset

    @classmethod
    def _sorted_levels(
        cls, levels: Iterable[OrderBookLevelLike], is_asks: bool
    ) -> List[OrderBookLevel]:
        normalized_levels = [OrderBookLevel.from_any(level) for level in levels]
        normalized_levels = [
            level for level in normalized_levels if level.size_float > 0
        ]
        return sorted(
            normalized_levels,
            key=lambda level: level.price_float,
            reverse=not is_asks,
        )

    @classmethod
    def _merge_levels(
        cls,
        existing_levels: Iterable[OrderBookLevel],
        new_levels: Iterable[OrderBookLevelLike],
        is_asks: bool,
    ) -> List[OrderBookLevel]:
        merged_by_price = {
            level.price: level for level in cls._sorted_levels(existing_levels, is_asks)
        }

        for new_level in new_levels:
            normalized_level = OrderBookLevel.from_any(new_level)
            if normalized_level.size_float == 0:
                merged_by_price.pop(normalized_level.price, None)
                continue
            merged_by_price[normalized_level.price] = normalized_level

        return cls._sorted_levels(merged_by_price.values(), is_asks=is_asks)
