import asyncio
import time

import lighter
from examples.utils import get_api_key_config

# The account's L1 private key: only the L1 wallet can set or loosen API key restrictions.
ETH_PRIVATE_KEY = "1234567812345678123456781234567812345678123456781234567812345678"


async def main():
    endpoint_profile, account_index, private_keys = get_api_key_config()
    api_key_index = next(iter(private_keys))
    client = lighter.SignerClient(
        url=endpoint_profile.api_url,
        account_index=account_index,
        api_private_keys=private_keys,
        chain_id=endpoint_profile.chain_id,
    )

    # Restrict the key to markets 0 and 1 and a 30-day expiry.
    # allowed_ips=["203.0.113.7"] would also limit the key's auth tokens to that IP,
    # so the lookup below would then only return restrictions when run from it.
    resp, err = await client.set_api_key_restrictions(
        ETH_PRIVATE_KEY,
        api_key_index,
        market_ids=[0, 1],
        valid_until=int(time.time()) + 30 * 24 * 3600,
    )
    print(resp, err)

    # Restrictions are returned only with auth for the account.
    auth, err = client.create_auth_token_with_expiry(api_key_index=api_key_index)
    keys = await lighter.AccountApi(client.api_client).apikeys(
        account_index=account_index, api_key_index=api_key_index, authorization=auth
    )
    print(keys.api_keys[0].restrictions)

    # Clear all restrictions. Each update needs a strictly newer timestamp (unix seconds).
    await asyncio.sleep(1)
    resp, err = await client.set_api_key_restrictions(ETH_PRIVATE_KEY, api_key_index)
    print(resp, err)

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())
