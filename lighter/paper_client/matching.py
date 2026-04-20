from math import fabs, pow
from typing import Iterable, List, Tuple

from lighter.paper_client.order_book import OrderBookLevel
from lighter.paper_client.types import (
    MarketConfig,
    PaperFill,
    PaperOrderRequest,
    PaperOrderSide,
    PaperOrderType,
)


def simulate_match(
    request: PaperOrderRequest,
    asks: Iterable[OrderBookLevel],
    bids: Iterable[OrderBookLevel],
    config: MarketConfig,
) -> Tuple[List[PaperFill], float]:
    remaining = request.base_amount
    fills: List[PaperFill] = []
    levels = asks if request.side == PaperOrderSide.BUY else bids

    for level in levels:
        if remaining <= 0:
            break

        try:
            level_price = level.price_float
            level_size = level.size_float
        except ValueError:
            continue

        if level_price <= 0 or level_size <= 0:
            continue

        if request.order_type == PaperOrderType.IOC:
            if request.side == PaperOrderSide.BUY and level_price > request.price:
                break
            if request.side == PaperOrderSide.SELL and level_price < request.price:
                break

        fill_size = min(remaining, level_size)
        fills.append(
            PaperFill(
                price=level_price,
                size=fill_size,
                fee=fill_size * level_price * config.taker_fee,
            )
        )
        remaining -= fill_size

    return fills, remaining


def validate_order(request: PaperOrderRequest, config: MarketConfig) -> None:
    if request.base_amount <= 0:
        raise ValueError(f"base amount must be positive, got {request.base_amount}")

    if not _fits_decimals(request.base_amount, config.size_decimals):
        raise ValueError(
            f"base amount {request.base_amount} exceeds "
            f"{config.size_decimals} size decimals for {config.symbol}"
        )

    if request.order_type == PaperOrderType.IOC:
        if request.price <= 0:
            raise ValueError(f"IoC order requires positive price, got {request.price}")
        if not _fits_decimals(request.price, config.price_decimals):
            raise ValueError(
                f"price {request.price} exceeds "
                f"{config.price_decimals} price decimals for {config.symbol}"
            )


def _fits_decimals(value: float, decimals: int) -> bool:
    multiplier = pow(10, decimals)
    rounded = round(value * multiplier) / multiplier
    return fabs(rounded - value) <= 1e-12
