"""Paper trading — live mode.

Subscribes to real-time order book updates via WebSocket and simulates
trades against continuously updated book state.

The paper client manages its own internal WebSocket listener and
sorted order book.
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

    # Start live tracking — connects a WebSocket and waits for the initial
    # order book snapshot before returning.
    await paper.track_market(market_id=0)  # ETH-PERP
    print("Live tracking started for ETH-PERP")

    # Wait a moment to accumulate order book updates
    await asyncio.sleep(2)

    # Place a market buy
    result = await paper.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=0,
            side=lighter.PaperOrderSide.BUY,
            base_amount=0.1,
        )
    )
    print(f"BUY  filled={result.filled_size}  avg_price={result.avg_price:.2f}")

    # Let the book update for a bit, then close with a sell
    await asyncio.sleep(2)

    result = await paper.create_paper_order(
        lighter.PaperOrderRequest(
            market_id=0,
            side=lighter.PaperOrderSide.SELL,
            base_amount=0.1,
        )
    )
    print(f"SELL filled={result.filled_size}  avg_price={result.avg_price:.2f}")

    # Print final account state
    account = paper.get_account()
    print(f"\nCollateral: {account.collateral:.2f} USDC")
    print(f"Portfolio value: {paper.get_portfolio_value():.2f} USDC")

    # Stop tracking and clean up
    await paper.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
