import asyncio
import time

from examples.utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()

    tx, tx_hash, err = await client.create_order(
        market_index=0,
        client_order_index=0,
        base_amount=2100,  # 0.21 ETH
        price=4000_00,  # Highest acceptable price for each market order
        is_ask=False,
        order_type=client.ORDER_TYPE_TWAP,
        time_in_force=client.ORDER_TIME_IN_FORCE_GOOD_TILL_TIME,
        reduce_only=False,
        trigger_price=0,
        order_expiry=int(time.time() * 1000) + 10 * 60 * 1000,
    )
    print(f"Create TWAP Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
