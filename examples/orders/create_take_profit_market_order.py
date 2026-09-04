import asyncio

import lighter

from examples.utils import default_example_setup


async def wait_for_long_position(api_client, account_index, market_index):
    account_api = lighter.AccountApi(api_client)

    for _ in range(20):
        response = await account_api.account(
            by="index",
            value=str(account_index),
            active_only=True,
        )
        if any(
            position.market_id == market_index
            and position.sign == 1
            and float(position.position) > 0
            for account in response.accounts
            for position in account.positions
        ):
            return
        await asyncio.sleep(0.5)

    raise RuntimeError("The entry order did not create a long position")


async def main():
    client, api_client, _ = default_example_setup()

    try:
        market_index = 0
        base_amount = 500

        entry_tx, entry_response, err = await client.create_market_order(
            market_index=market_index,
            client_order_index=0,
            base_amount=base_amount,
            avg_execution_price=4000_00,
            is_ask=False,
        )
        print(f"Create Entry Order {entry_tx=} {entry_response=} {err=}")
        if err is not None:
            raise Exception(err)

        await wait_for_long_position(api_client, client.account_index, market_index)

        tx, tx_hash, err = await client.create_tp_order(
            market_index=market_index,
            client_order_index=1,
            base_amount=base_amount,
            trigger_price=3500_00,
            price=3395_00,
            is_ask=True,
            reduce_only=True,
        )
        print(f"Create Take Profit Order {tx=} {tx_hash=} {err=}")
        if err is not None:
            raise Exception(err)
    finally:
        await client.close()
        await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
