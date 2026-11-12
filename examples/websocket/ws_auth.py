import json
import logging
import asyncio
import lighter
from examples.utils import get_api_key_config


def on_order_book_update(market_id, order_book):
    logging.info(f"Order book {market_id}:\n{json.dumps(order_book, indent=2)}")


def on_account_update(account_id, account):
    logging.info(f"Account {account_id}:\n{json.dumps(account, indent=2)}")


async def main():
    logging.basicConfig(level=logging.INFO)

    profile, account_index, private_keys = get_api_key_config()
    client = lighter.SignerClient(
        url=profile.api_url,
        account_index=account_index,
        api_private_keys=private_keys,
        chain_id=profile.chain_id,
    )

    # Authenticating the connection applies your account tier's websocket limits instead of the public ones.
    # The token only has to be valid when the connection opens.
    auth_token, err = client.create_auth_token_with_expiry()
    if err is not None:
        raise Exception(err)

    ws_client = lighter.WsClient(
        ws_url=profile.ws_url,
        order_book_ids=[0, 1],
        account_ids=[account_index],
        on_order_book_update=on_order_book_update,
        on_account_update=on_account_update,
        auth_token=auth_token,
    )

    try:
        await ws_client.run_async()
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
