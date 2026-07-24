import asyncio, json, lighter
from examples.utils import default_example_setup

async def main():
    client, api_client, _ = default_example_setup()
    auth_token, err = client.create_auth_token_with_expiry()
    assert err is None

    # set_maker_only_api_keys replaces the full set of maker-only API key indexes for the account.
    # Pass "[]" to clear all maker-only restrictions on the account
    # For set_maker_only_api_keys you can call this endpoint only once per hour
    # Indexes must be >= 4 e.g [4, 5, 6]

    account_api = lighter.AccountApi(api_client)

    resp = await account_api.set_maker_only_api_keys(
        account_index=client.account_index,
        api_key_indexes=json.dumps([4, 5, 6]),
        authorization=auth_token,
    )
    print("set:", resp)

    await asyncio.sleep(1)

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
    print("set:", resp)
    await asyncio.sleep(1)

    resp = await account_api.get_maker_only_api_keys(
        account_index=client.account_index,
        authorization=auth_token,
    )
    print("get:", resp)


    await client.close()
    await api_client.close()

if __name__ == "__main__":
    asyncio.run(main())
