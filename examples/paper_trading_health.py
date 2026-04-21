"""Paper trading — cross-market health & liquidation inspection.

Demonstrates how account health and liquidation prices change for the
same two-market portfolio under different collateral levels. Runs two
cross-margin scenarios:
  1. Conservative — large collateral, modest ETH + BTC exposure
  2. Aggressive — smaller collateral, larger ETH + BTC exposure
"""

import asyncio
import lighter

ETH_MARKET_ID = 0
BTC_MARKET_ID = 1
MARKETS = [
    (ETH_MARKET_ID, "ETH-PERP"),
    (BTC_MARKET_ID, "BTC-PERP"),
]


def round_size(size: float, decimals: int) -> float:
    return round(size, decimals)


def size_for_notional(
    paper: lighter.PaperClient,
    market_id: int,
    notional_usdc: float,
) -> float:
    config = paper.market_configs[market_id]
    raw_size = notional_usdc / config.last_trade_price
    return max(round_size(raw_size, config.size_decimals), config.min_base_amount)


async def track_markets(paper: lighter.PaperClient, markets: list[tuple[int, str]]) -> None:
    for market_id, _ in markets:
        await paper.track_market_snapshot(market_id)


def print_health(paper: lighter.PaperClient, markets: list[tuple[int, str]]) -> None:
    health = paper.get_health()
    print(f"  Health status:         {health.status.name}")
    print(f"  Total account value:   {health.total_account_value:.2f} USDC")
    print(f"  Initial margin req:    {health.initial_margin_requirement:.2f} USDC")
    print(f"  Maintenance margin:    {health.maintenance_margin_requirement:.2f} USDC")
    print(f"  Margin usage:          {health.margin_usage:.2f}%")
    print(f"  Leverage:              {health.leverage:.2f}x")

    for market_id, label in markets:
        position = paper.get_position(market_id)
        if position is not None and position.size != 0:
            liq_price = paper.get_liquidation_price(market_id)
            liq_str = f"${liq_price:.2f}" if liq_price > 0 else "n/a (fully collateralized)"
            side = "LONG" if position.size > 0 else "SHORT"
            print(
                f"  {label} {side} {abs(position.size):g}"
                f"  entry=${position.avg_entry_price:.2f}"
                f"  mark=${position.mark_price:.2f}"
                f"  unrealized_pnl={position.unrealized_pnl:.2f}"
                f"  liq_price={liq_str}"
            )

    print(f"  Portfolio value:       {paper.get_portfolio_value():.2f} USDC")
    print(f"  Collateral:            {paper.get_collateral():.2f} USDC")


async def main():
    api_client = lighter.ApiClient(
        configuration=lighter.Configuration(
            host="https://mainnet.zklighter.elliot.ai",
        ),
    )

    # ── Scenario 1: Conservative (low leverage) ──────────────────────
    # $10,000 collateral backing a modest ETH long + BTC short.
    # The portfolio stays lightly levered with wide or nonexistent
    # liquidation thresholds.
    print("=" * 60)
    print("SCENARIO 1: Conservative — $10,000 collateral, ETH + BTC portfolio")
    print("=" * 60)

    conservative = lighter.PaperClient(api_client, initial_collateral_usdc=10_000)
    await track_markets(conservative, MARKETS)

    conservative_eth_size = size_for_notional(conservative, ETH_MARKET_ID, 1_500)
    conservative_btc_size = size_for_notional(conservative, BTC_MARKET_ID, 1_000)

    await conservative.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=ETH_MARKET_ID,
            side=lighter.PaperOrderSide.BUY,
            base_amount=conservative_eth_size,
        )
    )
    await conservative.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=BTC_MARKET_ID,
            side=lighter.PaperOrderSide.SELL,
            base_amount=conservative_btc_size,
        )
    )
    print(
        f"Opened {conservative_eth_size:g} ETH long and "
        f"{conservative_btc_size:g} BTC short."
    )
    print_health(conservative, MARKETS)

    # ── Scenario 2: Aggressive (high leverage) ───────────────────────
    # $1,500 collateral backing the same market mix at much larger size.
    # Cross-margin still shares collateral across both markets, but
    # liquidation prices should move much closer to the current marks.
    print()
    print("=" * 60)
    print("SCENARIO 2: Aggressive — $1,500 collateral, same markets at larger size")
    print("=" * 60)

    aggressive = lighter.PaperClient(api_client, initial_collateral_usdc=1_500)
    await track_markets(aggressive, MARKETS)

    aggressive_eth_size = size_for_notional(aggressive, ETH_MARKET_ID, 6_000)
    aggressive_btc_size = size_for_notional(aggressive, BTC_MARKET_ID, 3_000)

    await aggressive.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=ETH_MARKET_ID,
            side=lighter.PaperOrderSide.BUY,
            base_amount=aggressive_eth_size,
        )
    )
    await aggressive.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=BTC_MARKET_ID,
            side=lighter.PaperOrderSide.SELL,
            base_amount=aggressive_btc_size,
        )
    )
    print(
        f"Opened {aggressive_eth_size:g} ETH long and "
        f"{aggressive_btc_size:g} BTC short."
    )
    print_health(aggressive, MARKETS)

    # Show the contrast
    print()
    print("-" * 60)
    print("COMPARISON")
    for market_id, label in MARKETS:
        cons_liq = conservative.get_liquidation_price(market_id)
        aggr_liq = aggressive.get_liquidation_price(market_id)
        aggr_pos = aggressive.get_position(market_id)
        cons_liq_str = "n/a (can't be liquidated)" if cons_liq == 0 else f"${cons_liq:.2f}"
        print(f"  {label} conservative liq: {cons_liq_str}")
        if aggr_pos is None:
            reason = "already liquidated" if aggressive.get_health().has_been_liquidated else "no open position"
            print(f"  {label} aggressive:       {reason}")
        else:
            distance = abs(aggr_pos.mark_price - aggr_liq)
            print(
                f"  {label} aggressive liq:   ${aggr_liq:.2f}  "
                f"(${distance:.2f} from mark)"
            )
    print("-" * 60)

    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
