import asyncio
from examples.utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()

    # Disable Unified Trading Account (mode=0, back to Simple)
    tx, response, err = await client.update_account_config(account_trading_mode=0)
    print(f"Disable UTA: {tx=} {response=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())