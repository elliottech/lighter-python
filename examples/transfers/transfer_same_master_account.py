import asyncio
import lighter
from examples.utils import default_example_setup

TO_ACCOUNT_INDEX = 281474976710648 # same master account


async def main():
    client, api_client, _ = default_example_setup()
    info_api = lighter.InfoApi(api_client)

    auth_token, err = client.create_auth_token_with_expiry()
    if err:
        raise Exception(f"Auth token failed: {err}")

    fee_info = await info_api.transfer_fee_info(client.account_index, authorization=auth_token, auth=auth_token, to_account_index=TO_ACCOUNT_INDEX)

    # You can find more notes on transfers in the README.md file, under `Transfer Notes`
    transfer_tx, response, err = await client.transfer_same_master_account(
        to_account_index=TO_ACCOUNT_INDEX,
        asset_id=client.ASSET_ID_USDC,
        route_from=client.ROUTE_PERP,
        route_to=client.ROUTE_PERP,
        amount=5,  # decimals are added by sdk
        fee=fee_info.transfer_fee_usdc,
        memo="0x" + "00" * 32,
    )
    if err is not None:
        raise Exception(f"error transferring {err}")

    print(transfer_tx, response)
    await client.close()
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
