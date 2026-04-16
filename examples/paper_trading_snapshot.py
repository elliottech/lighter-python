"""Paper trading — snapshot mode.

Fetches a one-time order book snapshot and simulates trades against it.
No API keys or signing required; only read-only API access is used.
"""

import asyncio
import lighter


async def main():
    api_client = lighter.ApiClient(
        configuration=lighter.Configuration(
            host="https://mainnet.zklighter.elliot.ai",
        ),
    )

    paper = lighter.PaperClient(api_client, initial_collateral_usdc=10_000)

    # Load a snapshot of the ETH-PERP order book (market_id=0)
    await paper.track_market_snapshot(market_id=0)

    # Simulate a market buy for 0.5 ETH
    result = await paper.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=0,
            side=lighter.PaperOrderSide.BUY,
            base_amount=0.5,
        )
    )
    print(f"BUY  filled={result.filled_size}  avg_price={result.avg_price:.2f}  fee={result.total_fee:.4f}")

    # Simulate a market sell to close the position
    result = await paper.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=0,
            side=lighter.PaperOrderSide.SELL,
            base_amount=0.5,
        )
    )
    print(f"SELL filled={result.filled_size}  avg_price={result.avg_price:.2f}  fee={result.total_fee:.4f}")

    # Print account summary
    account = paper.get_account()
    print(f"\nCollateral: {account.collateral:.2f} USDC")
    print(f"Trades: {len(account.trades)}")
    for trade in account.trades:
        side = "BUY" if trade.side == lighter.PaperOrderSide.BUY else "SELL"
        print(f"  {side} {trade.size} @ {trade.price:.2f}  pnl={trade.realized_pnl:.4f}")

    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
