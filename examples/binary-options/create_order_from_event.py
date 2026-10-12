import asyncio
import time
import lighter
from examples.utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()

    # Binary options markets are not listed by /orderBooks, discover them through /events.
    # Pick the active market that resolves soonest (end_timestamp is in ms).
    events = await lighter.EventApi(api_client).events(active=True, limit=10)
    now_ms = int(time.time() * 1000)
    market = min(
        (ob for event in events.events for ob in event.order_books if ob.status == "active" and ob.end_timestamp > now_ms),
        key=lambda ob: ob.end_timestamp,
    )
    print(
        f"{market.symbol} market_id={market.market_id} settlement_cap={market.settlement_cap} "
        f"best_bid={market.stats.best_bid_price} best_ask={market.stats.best_ask_price}"
    )

    # Prices are ticks between 0 and settlement_cap (the payout of a winning share).
    # Buy = YES, sell = NO. 60% of the cap == 0.60 implied probability.
    price = market.settlement_cap * 60 // 100
    base_amount = 10 * 10**market.size_decimals  # 10 shares

    tx, tx_hash, err = await client.create_order(
        market_index=market.market_id,
        client_order_index=0,
        base_amount=base_amount,
        price=price,
        is_ask=False,
        order_type=client.ORDER_TYPE_LIMIT,
        time_in_force=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
    )
    print(f"Create Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
