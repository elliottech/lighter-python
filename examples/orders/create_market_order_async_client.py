import asyncio

import lighter
from examples.utils import get_api_key_config, trim_exception


async def create_signer_for_user(config_file="./api_key_config.json"):
    # Constructing the SignerClient performs no network I/O (nonces are
    # fetched lazily on first use), so it is safe inside a coroutine.
    base_url, account_index, private_keys = get_api_key_config(config_file)
    client = lighter.SignerClient(
        url=base_url,
        account_index=account_index,
        api_private_keys=private_keys,
    )

    err = client.check_client()
    if err is not None:
        await client.close()
        raise Exception(f"CheckClient error: {trim_exception(err)}")

    return client


async def place_market_order_for_user(config_file="./api_key_config.json"):
    client = await create_signer_for_user(config_file)

    try:
        # Note: change this to 2048 to trade spot ETH. Make sure you have at least 0.1 ETH to trade spot.
        market_index = 0

        tx, tx_hash, err = await client.create_market_order(
            market_index=market_index,
            client_order_index=0,
            base_amount=100,  # 0.1 ETH
            avg_execution_price=4000_00,  # $4000 -- worst acceptable price for the order
            is_ask=False,
        )
        print(f"Create Order {tx=} {tx_hash=} {err=}")
        if err is not None:
            raise Exception(err)
    finally:
        await client.close()


async def main():
    await place_market_order_for_user()


if __name__ == "__main__":
    asyncio.run(main())
