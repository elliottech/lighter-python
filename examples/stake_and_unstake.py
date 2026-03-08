import asyncio

from utils import default_example_setup

STAKING_POOL_INDEX = 281474976624800


async def main():
    client, api_client, _ = default_example_setup()

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    try:
        tx_info, response, err = await client.stake_assets(public_pool_index=STAKING_POOL_INDEX, share_amount=10_000)
        if err is not None:
            raise Exception(f'failed to stake assets {err}')

        tx_info, response, err = await client.unstake_assets(public_pool_index=STAKING_POOL_INDEX, share_amount=10_000)
        if err is not None:
            raise Exception(f'failed to unstake assets {err}')
    finally:
        await client.close()
        await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
