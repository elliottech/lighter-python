import asyncio
import os
import time
from examples.utils import default_example_setup


CONFIG = os.path.join(os.path.dirname(__file__), "..", "api_key_config.json")
approval_expiry = int(time.time() * 1000) + 90 * 24 * 60 * 60 * 1000  # now + 90 days, in ms


async def main():
    client, api_client, _ = default_example_setup(config_file=CONFIG)

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    # L2-only approve: no eth_private_key, signed with the API (L2) key only.
    # integrator_account_index must be a SUB-ACCOUNT under your own master account (same L1 owner).
    # This is what lets the approve go through with L2 sig only (no eth_private_key).
    tx_info, response, err = await client.approve_integrator(
        integrator_account_index=6,
        max_perps_taker_fee=1000,
        max_perps_maker_fee=1000,
        max_spot_taker_fee=1000,
        max_spot_maker_fee=1000,
        approval_expiry=approval_expiry,
    )
    print(tx_info, response, err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())