import asyncio
import os
import time
from examples.utils import default_example_setup


CONFIG_FILE = "../api_key_config.json"
APPROVAL_EXPIRY = int(time.time() * 1000) + 90 * 24 * 60 * 60 * 1000  # now + 90 days, in ms


async def main():
    client, api_client, _ = default_example_setup(CONFIG_FILE)

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    # no L1 sig required if integrator takes no fees
    tx_info, response, err = await client.approve_integrator(
        integrator_account_index=6,
        max_perps_taker_fee=0,
        max_perps_maker_fee=0,
        max_spot_taker_fee=0,
        max_spot_maker_fee=0,
        approval_expiry=APPROVAL_EXPIRY,
    )
    print(tx_info, response, err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())