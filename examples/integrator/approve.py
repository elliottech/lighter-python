import asyncio
import time
from examples.utils import default_example_setup


ETH_PRIVATE_KEY = ""
CONFIG_FILE = "../api_key_config.json"
APPROVAL_EXPIRY = int(time.time() * 1000) + 90 * 24 * 60 * 60 * 1000  # now + 90 days, in ms


async def main():
    client, api_client, _ = default_example_setup(CONFIG_FILE)

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
        approval_expiry=APPROVAL_EXPIRY
    )
    print(tx_info, response, err)

    await client.close()
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())