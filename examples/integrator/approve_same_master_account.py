import asyncio
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

    # no L1 sig required for approving integrator who is tied to the same address (e.g. subaccount)
    tx_info, response, err = await client.approve_integrator(
        integrator_account_index=281474976710649,
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