import asyncio
from utils import default_example_setup


async def main():
    client, api_client, _ = default_example_setup()

    tx, resp, err = await client.update_account_asset_config(
        asset_index=client.ASSET_ID_ETH,
        asset_margin_mode=client.ASSET_MARGIN_MODE_DISABLED,
    )
    print(f"Enable ETH as margin: {tx=} {resp=} {err=}")
    if err is not None:
        raise Exception(err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())