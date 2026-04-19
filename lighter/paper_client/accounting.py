from dataclasses import replace
from math import fabs
from typing import Dict, Optional

from lighter.paper_client.types import (
    PaperAccount,
    PaperOrderSide,
    PaperPosition,
    PaperTrade,
    utc_now,
)


def new_paper_account(collateral_usdc: float) -> PaperAccount:
    return PaperAccount(
        initial_collateral=collateral_usdc,
        collateral=collateral_usdc,
    )


def copy_position(position: Optional[PaperPosition]) -> Optional[PaperPosition]:
    return replace(position) if position is not None else None


def copy_account(account: PaperAccount) -> PaperAccount:
    return PaperAccount(
        initial_collateral=account.initial_collateral,
        collateral=account.collateral,
        positions={
            market_id: replace(position)
            for market_id, position in account.positions.items()
        },
        trades=list(account.trades),
        has_been_liquidated=account.has_been_liquidated,
    )


def apply_fill(
    account: PaperAccount,
    market_id: int,
    side: PaperOrderSide,
    fill_size: float,
    fill_price: float,
    fee: float,
    *,
    is_liquidation: bool = False,
) -> float:
    position = account.positions.get(market_id)
    if position is None:
        position = PaperPosition(market_id=market_id)
        account.positions[market_id] = position

    old_position = position.size
    old_abs_size = fabs(old_position)
    old_entry_quote = position.entry_quote

    position_delta = fill_size if side == PaperOrderSide.BUY else -fill_size
    new_position = old_position + position_delta
    new_abs_size = fabs(new_position)

    old_sign = sign(old_position)
    new_sign = sign(new_position)
    realized_pnl = 0.0
    new_entry_quote = 0.0

    if old_sign == 0:
        new_entry_quote = fill_size * fill_price
    elif old_sign != new_sign and new_sign != 0:
        realized_pnl = _full_close_pnl(old_sign, old_abs_size, old_entry_quote, fill_price)
        new_entry_quote = new_abs_size * fill_price
    elif old_sign != new_sign and new_sign == 0:
        realized_pnl = _full_close_pnl(old_sign, old_abs_size, old_entry_quote, fill_price)
    elif new_abs_size > old_abs_size:
        new_entry_quote = old_entry_quote + fill_size * fill_price
    else:
        if old_abs_size > 0:
            new_entry_quote = old_entry_quote * (new_abs_size / old_abs_size)
            closed_size = old_abs_size - new_abs_size
            avg_entry = old_entry_quote / old_abs_size
            if old_sign > 0:
                realized_pnl = closed_size * fill_price - closed_size * avg_entry
            else:
                realized_pnl = closed_size * avg_entry - closed_size * fill_price

    position.size = new_position
    position.entry_quote = new_entry_quote
    position.avg_entry_price = new_entry_quote / new_abs_size if new_abs_size > 0 else 0
    position.realized_pnl += realized_pnl

    account.collateral += realized_pnl
    account.collateral -= fee
    account.trades.append(
        PaperTrade(
            market_id=market_id,
            side=side,
            size=fill_size,
            price=fill_price,
            fee=fee,
            realized_pnl=realized_pnl,
            is_liquidation=is_liquidation,
            timestamp=utc_now(),
        )
    )
    if is_liquidation:
        account.has_been_liquidated = True

    if abs(new_position) < 1e-12:
        del account.positions[market_id]

    return realized_pnl


def compute_unrealized_pnl(position: Optional[PaperPosition], mark_price: float) -> float:
    if position is None or position.size == 0:
        return 0.0

    abs_size = fabs(position.size)
    position_value = abs_size * mark_price
    if position.size > 0:
        return position_value - position.entry_quote
    return position.entry_quote - position_value


def compute_total_account_value(
    account: PaperAccount,
    mark_prices: Dict[int, float],
) -> float:
    total = account.collateral
    for market_id, position in account.positions.items():
        mark_price = mark_prices.get(market_id)
        if mark_price is not None:
            total += compute_unrealized_pnl(position, mark_price)
    return total


def sign(value: float) -> int:
    if value > 0:
        return 1
    if value < 0:
        return -1
    return 0


def _full_close_pnl(
    old_sign: int,
    old_abs_size: float,
    old_entry_quote: float,
    fill_price: float,
) -> float:
    if old_sign > 0:
        return old_abs_size * fill_price - old_entry_quote
    return old_entry_quote - old_abs_size * fill_price
