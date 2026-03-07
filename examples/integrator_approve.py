import asyncio
from utils import default_example_setup


ETH_PRIVATE_KEY = ""

async def main():
    client, api_client, _ = default_example_setup()

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    tx_info, response, err = await client.approve_integrator(
        eth_private_key=ETH_PRIVATE_KEY,
        integrator_account_index=6,
        max_perps_taker_fee=1000,
        max_perps_maker_fee=1000,
        max_spot_taker_fee=1000,
        max_spot_maker_fee=1000,
        approval_expiry=1775518466000
    )
    print(tx_info, response, err)

    await client.close()
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())