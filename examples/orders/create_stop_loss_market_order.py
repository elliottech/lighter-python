import asyncio

from examples.utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()

    tx, tx_hash, err = await client.create_sl_order(
        market_index=0,
        client_order_index=0,
        base_amount=1000,  # 0.1 ETH
        trigger_price=2500_00,  # Trigger when ETH reaches $2500
        price=2425_00,  # Lowest acceptable execution price
        is_ask=True,
        reduce_only=True,
    )
    print(f"Create Stop Loss Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
