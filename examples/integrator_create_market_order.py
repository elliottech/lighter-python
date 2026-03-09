import asyncio
from utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()
    client.check_client()

    # Note: change this to 2048 to trade spot ETH. Make sure you have at least 0.1 ETH to trade spot.
    market_index = 2048
    # integrator_account_index = 6
    integrator_account_index = 281474976710647
    integrator_taker_fee = 1000
    integrator_maker_fee = 500

    tx, tx_hash, err = await client.create_market_order(
        market_index=market_index,
        client_order_index=0,
        base_amount=1000,  # 0.1 ETH
        avg_execution_price=1900_00,
        is_ask=True,
        integrator_account_index=integrator_account_index,
        integrator_taker_fee=integrator_taker_fee,
        integrator_maker_fee=integrator_maker_fee,
    )
    print(f"Create Order {tx=} {tx_hash=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
