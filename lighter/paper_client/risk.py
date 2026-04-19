from math import fabs
from typing import List

from lighter.paper_client.accounting import (
    apply_fill,
    compute_total_account_value,
    compute_unrealized_pnl,
)
from lighter.paper_client.types import (
    MarketConfigMap,
    MarkPriceMap,
    PaperAccount,
    PaperAccountHealth,
    PaperHealthStatus,
    PaperOrderSide,
)


def compute_initial_margin_requirement(
    account: PaperAccount,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> float:
    total = 0.0
    for market_id, position in account.positions.items():
        mark_price = mark_prices.get(market_id)
        config = configs.get(market_id)
        if mark_price is None or config is None:
            continue
        total += (
            fabs(position.size)
            * mark_price
            * (config.default_initial_margin_fraction / 10_000)
        )
    return total


def compute_maintenance_margin_requirement(
    account: PaperAccount,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> float:
    total = 0.0
    for market_id, position in account.positions.items():
        mark_price = mark_prices.get(market_id)
        config = configs.get(market_id)
        if mark_price is None or config is None:
            continue
        total += (
            fabs(position.size)
            * mark_price
            * (config.maintenance_margin_fraction / 10_000)
        )
    return total


def compute_closeout_margin_requirement(
    account: PaperAccount,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> float:
    total = 0.0
    for market_id, position in account.positions.items():
        mark_price = mark_prices.get(market_id)
        config = configs.get(market_id)
        if mark_price is None or config is None:
            continue
        total += (
            fabs(position.size)
            * mark_price
            * (config.closeout_margin_fraction / 10_000)
        )
    return total


def compute_health(
    account: PaperAccount,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> PaperAccountHealth:
    tav = compute_total_account_value(account, mark_prices)
    imr = compute_initial_margin_requirement(account, mark_prices, configs)
    mmr = compute_maintenance_margin_requirement(account, mark_prices, configs)

    if tav < 0:
        status = PaperHealthStatus.BANKRUPTCY
    # Not in scope for paper trading
    # elif tav < comr:
    #     status = PaperHealthStatus.FULL_LIQUIDATION
    # elif tav < mmr:
    #     status = PaperHealthStatus.PARTIAL_LIQUIDATION
    elif tav < imr:
        status = PaperHealthStatus.PRE_LIQUIDATION
    else:
        status = PaperHealthStatus.HEALTHY

    if imr == 0:
        margin_usage = 0.0
    elif tav > 0:
        margin_usage = imr / tav * 100
    else:
        margin_usage = float("inf")
    total_notional = 0.0
    for market_id, position in account.positions.items():
        mark_price = mark_prices.get(market_id)
        if mark_price is not None:
            total_notional += fabs(position.size) * mark_price

    leverage = total_notional / tav if tav > 0 else 0.0
    return PaperAccountHealth(
        status=status,
        total_account_value=tav,
        initial_margin_requirement=imr,
        maintenance_margin_requirement=mmr,
        margin_usage=margin_usage,
        leverage=leverage,
        has_been_liquidated=account.has_been_liquidated,
    )


def compute_liquidation_price(
    account: PaperAccount,
    market_id: int,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> float:
    position = account.positions.get(market_id)
    config = configs.get(market_id)
    mark_price = mark_prices.get(market_id)
    if position is None or position.size == 0 or config is None or mark_price is None:
        return 0.0

    tav = compute_total_account_value(account, mark_prices)
    cross_mmr = compute_maintenance_margin_requirement(account, mark_prices, configs)
    abs_size = fabs(position.size)
    mm_fraction = config.maintenance_margin_fraction / 10_000
    position_sign = 1 if position.size > 0 else -1
    denominator = abs_size * (mm_fraction - position_sign)
    if denominator == 0:
        return 0.0

    liquidation_price = mark_price + (tav - cross_mmr) / denominator
    if liquidation_price < 0:
        return 0.0

    if position.size > 0 and liquidation_price >= mark_price:
        return mark_price
    if position.size < 0 and liquidation_price <= mark_price:
        return mark_price
    return liquidation_price


def check_and_liquidate(
    account: PaperAccount,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> List[int]:
    liquidated_market_ids: List[int] = []
    for market_id, position in list(account.positions.items()):
        liquidation_price = compute_liquidation_price(
            account,
            market_id,
            mark_prices,
            configs,
        )
        if liquidation_price == 0:
            continue

        mark_price = mark_prices.get(market_id)
        if mark_price is None:
            continue

        if position.size > 0 and mark_price <= liquidation_price:
            liquidated_market_ids.append(market_id)
        elif position.size < 0 and mark_price >= liquidation_price:
            liquidated_market_ids.append(market_id)

    for market_id in liquidated_market_ids:
        position = account.positions.get(market_id)
        mark_price = mark_prices[market_id]
        if position is None:
            continue

        close_side = PaperOrderSide.SELL if position.size > 0 else PaperOrderSide.BUY
        apply_fill(
            account,
            market_id,
            close_side,
            fabs(position.size),
            mark_price,
            0,
            is_liquidation=True,
        )

    return liquidated_market_ids


def update_position_metrics(
    account: PaperAccount,
    mark_prices: MarkPriceMap,
    configs: MarketConfigMap,
) -> None:
    for market_id, position in account.positions.items():
        mark_price = mark_prices.get(market_id)
        if mark_price is None:
            continue
        position.mark_price = mark_price
        position.unrealized_pnl = compute_unrealized_pnl(position, mark_price)
        position.liquidation_price = compute_liquidation_price(
            account,
            market_id,
            mark_prices,
            configs,
        )
