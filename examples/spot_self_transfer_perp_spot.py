import asyncio
from utils import default_example_setup

ETH_PRIVATE_KEY = "1234567812345678123456781234567812345678123456781234567812345678"


async def main():
    client, api_client, _ = default_example_setup()

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    memo = "a"*32  # memo is a user message, and it has to be exactly 32 bytes long
    transfer_tx, response, err = await client.transfer(
        ETH_PRIVATE_KEY,
        to_account_index=client.account_index,
        asset_id=client.ASSET_ID_USDC,
        amount=1.234567,  # decimals are added by sdk
        route_from=client.ROUTE_PERP,
        route_to=client.ROUTE_SPOT,
        fee=0,
        memo=memo,
    )
    if err is not None:
       raise Exception(f"error transferring {err}")
    print(transfer_tx, response)

    lev_tx, response, err = await client.update_leverage(4, client.CROSS_MARGIN_MODE, 3)
    print(lev_tx, response, err)

if __name__ == "__main__":
    asyncio.run(main())