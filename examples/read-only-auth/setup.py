import asyncio
import json
import sys
import eth_account
import lighter
import os

BASE_URL = os.getenv("BASE_URL", "https://testnet.zklighter.elliot.ai")
ETH_PRIVATE_KEY = os.getenv("ETH_PRIVATE_KEY", "")
API_KEY_INDEX = int(os.getenv("API_KEY_INDEX", "253"))
NUM_API_KEYS = int(os.getenv("NUM_API_KEYS", "1"))

async def setup_account(eth_private_key, account_index, base_url, api_key_index, num_keys):
    """
    Setup API keys for a single account.
    
    Args:
        eth_private_key: User's L1 Ethereum private key (for signing transactions)
        account_index: Account index on the exchange
        base_url: API base URL
        api_key_index: Starting API key index
        num_keys: Number of API keys to generate and register
    
    Returns:
        Tuple of (config_dict, error_string)
    """
    try:
        private_keys = {}
        public_keys = {}
        
        for i in range(num_keys):
            idx = api_key_index + i
            private_key, public_key, err = lighter.create_api_key()
            if err is not None:
                return None, f"Failed to create API key {idx}: {err}"
            private_keys[idx] = private_key
            public_keys[idx] = public_key
        
        tx_client = lighter.SignerClient(
            url=base_url,
            account_index=account_index,
            api_private_keys=private_keys,
        )
        
        for idx, pub_key in public_keys.items():
            response, err = await tx_client.change_api_key(
                eth_private_key=eth_private_key,
                new_pubkey=pub_key,
                api_key_index=idx,
            )
            if err is not None:
                await tx_client.close()
                return None, f"Failed to register API key {idx}: {err}"
        
        await asyncio.sleep(5)
        
        err = tx_client.check_client()
        await tx_client.close()
        if err is not None:
            return None, f"Failed to verify API keys: {err}"
        
        return {
            "account_index": account_index,
            "api_key_indices": list(private_keys.keys()),
            "api_key_private_keys": private_keys,
        }, None
    
    except Exception as e:
        return None, f"Exception in setup_account: {str(e)}"


async def main():
    if not ETH_PRIVATE_KEY or not BASE_URL:
        print("Error: ETH_PRIVATE_KEY and BASE_URL environment variables are required")
        return
    
    config_file = "config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    api_client = lighter.ApiClient(configuration=lighter.Configuration(host=BASE_URL))
    eth_acc = eth_account.Account.from_key(ETH_PRIVATE_KEY)
    eth_address = eth_acc.address
    
    try:
        response = await lighter.AccountApi(api_client).accounts_by_l1_address(
            l1_address=eth_address
        )
    except lighter.ApiException as e:
        if e.data.message == "account not found":
            print(f"Error: account not found for {eth_address}", file=__import__('sys').stderr)
            await api_client.close()
            return
        else:
            await api_client.close()
            raise e
    
    if len(response.sub_accounts) == 0:
        print(f"Error: no accounts found for {eth_address}", file=__import__('sys').stderr)
        await api_client.close()
        return
    
    accounts = []
    for sub_account in response.sub_accounts:
        result, err = await setup_account(
            ETH_PRIVATE_KEY,
            int(sub_account.index),
            BASE_URL,
            API_KEY_INDEX,
            NUM_API_KEYS,
        )
        
        if err is not None:
            print(f"error: failed to setup account {sub_account.index}: {err}", file=sys.stderr)
        else:
            accounts.append(result)
    
    if not accounts:
        print("Error: failed to setup any accounts", file=__import__('sys').stderr)
        await api_client.close()
        return
    
    config = {
        "BASE_URL": BASE_URL,
        "ACCOUNTS": accounts,
    }
    
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    await api_client.close()


if __name__ == "__main__":
    asyncio.run(main())
