import asyncio
from examples.utils import default_example_setup



async def main():
    client, api_client, _ = default_example_setup()

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    # You can find more notes on transfers in the README.md file, under `Transfer Notes`
    transfer_tx, response, err = await client.transfer_same_master_account(
        to_account_index=client.account_index,
        asset_id=client.ASSET_ID_USDC,
        amount=1.234567,  # decimals are added by sdk
        route_from=client.ROUTE_SPOT,
        route_to=client.ROUTE_PERP,
        fee=0,
        memo="0x" + "00" * 32,
    )
    if err is not None:
       raise Exception(f"error transferring {err}")
    print(transfer_tx, response)

    lev_tx, response, err = await client.update_leverage(4, client.CROSS_MARGIN_MODE, 3)
    print(lev_tx, response, err)

    await client.close()
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())