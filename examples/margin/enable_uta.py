import asyncio
from examples.utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()

    # Enable Unified Trading Account (mode=1)
    tx, response, err = await client.update_account_config(account_trading_mode=1)
    print(f"Enable UTA: {tx=} {response=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())