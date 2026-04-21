import asyncio, json, lighter
from utils import default_example_setup

async def main():
    client, api_client, _ = default_example_setup()
    auth_token, err = client.create_auth_token_with_expiry()
    assert err is None

    account_api = lighter.AccountApi(api_client)

    resp = await account_api.set_maker_only_api_keys(
        account_index=client.account_index,
        api_key_indexes=json.dumps([4, 5, 6]),
        authorization=auth_token,
    )
    print("set:", resp)

    resp = await account_api.get_maker_only_api_keys(
        account_index=client.account_index,
        authorization=auth_token,
    )
    print("get:", resp)

    # clear maker only restrictions
    resp = await account_api.set_maker_only_api_keys(
        account_index=client.account_index,
        api_key_indexes=json.dumps([]),
        authorization=auth_token,
    )

    resp = await account_api.get_maker_only_api_keys(
        account_index=client.account_index,
        authorization=auth_token,
    )
    print("get:", resp)


    await client.close()
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())