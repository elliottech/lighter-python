"""Paper trading — health & liquidation inspection.

Demonstrates how account health and liquidation prices change
depending on leverage. Runs two scenarios:
  1. Conservative — large collateral, small position, no liquidation risk
  2. Aggressive — small collateral, large position, tight liquidation price
"""

import asyncio
import lighter


def print_health(paper: lighter.PaperClient, markets: list):
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
                f"  {label} {side} {abs(position.size)}"
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
    # $10,000 collateral backing a 0.5 ETH long → ~0.12x leverage.
    # The position is so over-collateralized that no liquidation price
    # exists (ETH would have to go below $0).
    print("=" * 60)
    print("SCENARIO 1: Conservative — $10,000 collateral, 0.5 ETH long")
    print("=" * 60)

    conservative = lighter.PaperClient(api_client, initial_collateral_usdc=10_000)
    await conservative.track_market_snapshot(market_id=0)

    await conservative.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=0,
            side=lighter.PaperOrderSide.BUY,
            base_amount=0.5,
        )
    )
    print_health(conservative, [(0, "ETH-PERP")])

    # ── Scenario 2: Aggressive (high leverage) ───────────────────────
    # $600 collateral backing a 4 ETH long → ~15x leverage.
    # Liquidation price will be tight — a ~5% drop would trigger it.
    print()
    print("=" * 60)
    print("SCENARIO 2: Aggressive — $600 collateral, 4 ETH long")
    print("=" * 60)

    aggressive = lighter.PaperClient(api_client, initial_collateral_usdc=600)
    await aggressive.track_market_snapshot(market_id=0)

    await aggressive.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=0,
            side=lighter.PaperOrderSide.BUY,
            base_amount=4.0,
        )
    )
    print_health(aggressive, [(0, "ETH-PERP")])

    # Show the contrast
    cons_liq = conservative.get_liquidation_price(0)
    aggr_liq = aggressive.get_liquidation_price(0)
    aggr_mark = aggressive.get_position(0).mark_price
    print()
    print("-" * 60)
    print("COMPARISON")
    cons_liq_str = "n/a (can't be liquidated)" if cons_liq == 0 else f"${cons_liq:.2f}"
    print(f"  Conservative liq price: {cons_liq_str}")
    print(f"  Aggressive liq price:   ${aggr_liq:.2f}  (${aggr_mark - aggr_liq:.2f} below mark)")
    print("-" * 60)

    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
