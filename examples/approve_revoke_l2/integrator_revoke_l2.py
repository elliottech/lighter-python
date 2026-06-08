import asyncio
import os
from examples.utils import default_example_setup

CONFIG = os.path.join(os.path.dirname(__file__), "..", "api_key_config.json")


async def main():
    client, api_client, _ = default_example_setup(config_file=CONFIG)

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    # Revoke = all fees 0 + expiry 0. No eth_private_key required, L2 sig only.
    tx_info, response, err = await client.approve_integrator(
        integrator_account_index=6,
        max_perps_taker_fee=0,
        max_perps_maker_fee=0,
        max_spot_taker_fee=0,
        max_spot_maker_fee=0,
        approval_expiry=0,
    )
    print(tx_info, response, err)

    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())