import asyncio
from examples.utils import default_example_setup


CONFIG_FILE = "../api_key_config.json"


async def main():
    client, api_client, _ = default_example_setup(CONFIG_FILE)

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    # no L1 sig required for revoking
    tx_info, response, err = await client.approve_integrator(
        integrator_account_index=281474976710649,
        max_perps_taker_fee=0,
        max_perps_maker_fee=0,
        max_spot_taker_fee=0,
        max_spot_maker_fee=0,
        approval_expiry=0
    )
    print(tx_info, response, err)

    await client.close()
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())