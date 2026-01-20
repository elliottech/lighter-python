import asyncio
import os
import json
import time
import lighter
import requests
from typing import Optional, Dict, Tuple
from eth_account import Account
from eth_utils import to_checksum_address
from eth_abi import encode
from utils import save_api_key_config

# Supported chains and their USDC contracts
CHAIN_CONFIGS = {
    42161: {"name": "Arbitrum", "usdc": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"},
    8453: {"name": "Base", "usdc": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"},
    43114: {"name": "Avalanche", "usdc": "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E"},
    999: {"name": "HyperEVM", "usdc": None},  # Add USDC contract when available
    101: {"name": "Solana", "usdc": None},  # Solana uses different approach
}

# Environment variables
BASE_URL = os.getenv("BASE_URL", "https://testnet.zklighter.elliot.ai")
ETH_PRIVATE_KEY = os.getenv("ETH_PRIVATE_KEY", "")
L2_RPC_URL = os.getenv("L2_RPC_URL", "")
CHAIN_ID = int(os.getenv("CHAIN_ID", "42161"))
USDC_CONTRACT = os.getenv("USDC_CONTRACT", "")
DEPOSIT_AMOUNT = float(os.getenv("DEPOSIT_AMOUNT", "6"))
OUTPUT_FILE = "api_key_config.json"
API_KEY_INDEX = int(os.getenv("API_KEY_INDEX", "4"))
NUM_API_KEYS = int(os.getenv("NUM_API_KEYS", "1"))


async def get_intent_address(l1_address: str, chain_id: int) -> Optional[str]:
    """Get intent address for deposit."""
    params = {
        "chain_id": str(chain_id),
        "from_addr": l1_address,
        "amount": "0",
        "is_external_deposit": "true"
    }
    response = requests.post(
        f"{BASE_URL}/api/v1/createIntentAddress",
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
    )
    if response.status_code == 200:
        data = response.json()
        return data.get("intent_address")
    return None


async def get_account(l1_address: str) -> Optional[Dict]:
    """Get account info including balance."""
    try:
        l1_address = to_checksum_address(l1_address)
        api_client = lighter.ApiClient(configuration=lighter.Configuration(host=BASE_URL))
        account_api = lighter.AccountApi(api_client)
        response = await account_api.accounts_by_l1_address(l1_address=l1_address)
        if response.sub_accounts and len(response.sub_accounts) > 0:
            accounts = response.sub_accounts
            master_account = min(accounts, key=lambda x: int(x.index))
            idx = int(master_account.index)
            if idx == 0:
                await api_client.close()
                return None
            account_details = await account_api.account(by="index", value=str(idx))
            await api_client.close()
            l2_addr = getattr(master_account, 'l2_address', None) or l1_address
            return {
                "accountIndex": idx,
                "l2Address": l2_addr,
                "availableBalance": getattr(account_details, "available_balance", "0")
            }
        await api_client.close()
        return None
    except Exception:
        return None


async def wait_for_account(l1_address: str) -> Optional[Dict]:
    """Wait for account to be created after deposit."""
    for i in range(60):
        account_info = await get_account(l1_address)
        if account_info:
            return account_info
        if i % 6 == 0:
            print(f"Waiting... ({i * 10 // 60}m)")
        await asyncio.sleep(10)
    return None


async def get_usdc_balance(wallet_address: str, usdc_address: str) -> float:
    """Get USDC balance on the chain."""
    decimals_selector = '0x313ce567'
    balance_selector = '0x70a08231'
    
    resp = requests.post(L2_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_address, "data": decimals_selector}, "latest"],
        "id": 1
    })
    decimals = int(resp.json()["result"], 16)
    
    data = balance_selector + wallet_address[2:].rjust(64, '0')
    resp = requests.post(L2_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_address, "data": data}, "latest"],
        "id": 1
    })
    balance = int(resp.json()["result"], 16)
    return balance / (10 ** decimals)


async def deposit_indirect(l1_address: str) -> bool:
    """Deposit USDC to intent address on external chain."""
    intent_addr = await get_intent_address(l1_address, CHAIN_ID)
    if not intent_addr:
        print("❌ Failed to get intent address")
        return False
    
    chain_config = CHAIN_CONFIGS.get(CHAIN_ID, {"name": f"Chain {CHAIN_ID}", "usdc": None})
    chain_name = chain_config["name"]
    usdc_address = to_checksum_address(USDC_CONTRACT or chain_config.get("usdc"))
    
    if not usdc_address:
        print(f"❌ USDC contract address required for {chain_name}")
        print("   Set USDC_CONTRACT environment variable")
        return False
    
    print(f"Intent Address ({chain_name}): {intent_addr}")
    
    account = Account.from_key(ETH_PRIVATE_KEY)
    wallet_address = to_checksum_address(account.address)
    intent_addr = to_checksum_address(intent_addr)
    
    # Check balance
    balance = await get_usdc_balance(wallet_address, usdc_address)
    if balance < DEPOSIT_AMOUNT:
        print(f"❌ Insufficient balance. Required: {DEPOSIT_AMOUNT}, Available: {balance}")
        return False
    
    decimals_selector = '0x313ce567'
    resp = requests.post(L2_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_address, "data": decimals_selector}, "latest"],
        "id": 1
    })
    decimals = int(resp.json()["result"], 16)
    amount_in_units = int(DEPOSIT_AMOUNT * (10 ** decimals))
    
    transfer_selector = '0xa9059cbb'
    transfer_data = transfer_selector + encode(['address', 'uint256'], [intent_addr, amount_in_units]).hex()
    
    nonce = int(requests.post(L2_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [wallet_address, "latest"],
        "id": 1
    }).json()["result"], 16)
    
    gas_price = int(requests.post(L2_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_gasPrice",
        "params": [],
        "id": 1
    }).json()["result"], 16)
    
    tx = {
        "to": usdc_address,
        "value": 0,
        "gas": 100000,
        "gasPrice": gas_price,
        "nonce": nonce,
        "chainId": CHAIN_ID,
        "data": transfer_data
    }
    signed = account.sign_transaction(tx)
    raw_tx = '0x' + signed.raw_transaction.hex()
    
    tx_hash = requests.post(L2_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_sendRawTransaction",
        "params": [raw_tx],
        "id": 1
    }).json().get("result")
    
    if not tx_hash:
        print("❌ Transfer failed")
        return False
    
    print(f"✅ Transfer tx: {tx_hash}")
    
    for _ in range(30):
        receipt = requests.post(L2_RPC_URL, json={
            "jsonrpc": "2.0",
            "method": "eth_getTransactionReceipt",
            "params": [tx_hash],
            "id": 1
        }).json().get("result")
        if receipt and receipt.get("status") == "0x1":
            return True
        await asyncio.sleep(2)
    
    return False


async def generate_api_keys(account_index: int) -> Tuple[Dict[int, str], Dict[int, str]]:
    """Generate API key pairs."""
    private_keys: Dict[int, str] = {}
    public_keys: Dict[int, str] = {}
    
    for i in range(NUM_API_KEYS):
        idx = API_KEY_INDEX + i
        private_key, public_key, err = lighter.create_api_key()
        if err is not None:
            raise Exception(f"Failed to generate API key: {err}")
        private_keys[idx] = private_key
        public_keys[idx] = public_key
    
    return private_keys, public_keys


async def register_api_keys(account_index: int, private_keys: Dict[int, str], public_keys: Dict[int, str]) -> bool:
    """Register API keys on the exchange."""
    try:
        tx_client = lighter.SignerClient(
            url=BASE_URL,
            account_index=account_index,
            api_private_keys=private_keys,
        )
        
        for idx, pub in public_keys.items():
            _, err = await tx_client.change_api_key(
                eth_private_key=ETH_PRIVATE_KEY,
                new_pubkey=pub,
                api_key_index=idx,
            )
            if err is not None:
                await tx_client.close()
                return False
        
        await asyncio.sleep(10)
        err = tx_client.check_client()
        await tx_client.close()
        return err is None
    except Exception as e:
        print(f"Failed to register API keys: {e}")
        return False


def save_config(account_index: str, l1_address: str, l2_address: str, private_keys: Dict[int, str]):
    """Save configuration to JSON file."""
    private_keys_dict = {str(k): v for k, v in private_keys.items()}
    save_api_key_config(BASE_URL, account_index, private_keys_dict, OUTPUT_FILE)
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
        config["l1_address"] = l1_address
        config["l2_address"] = l2_address
        config["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception:
        config = {
            "base_url": BASE_URL,
            "account_index": account_index,
            "private_keys": private_keys_dict,
            "l1_address": l1_address,
            "l2_address": l2_address,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)


async def main():
    if not ETH_PRIVATE_KEY or not L2_RPC_URL:
        print("❌ ETH_PRIVATE_KEY and L2_RPC_URL required")
        return
    
    chain_config = CHAIN_CONFIGS.get(CHAIN_ID, {"name": f"Chain {CHAIN_ID}"})
    chain_name = chain_config["name"]
    print(f"Using {chain_name} (Chain ID: {CHAIN_ID})")
    
    if not USDC_CONTRACT and not chain_config.get("usdc"):
        print(f"❌ USDC_CONTRACT required for {chain_name}")
        print("   Set USDC_CONTRACT environment variable")
        return
    
    account = Account.from_key(ETH_PRIVATE_KEY)
    l1_address = to_checksum_address(account.address)
    
    account_info = await get_account(l1_address)
    
    if account_info:
        balance = float(account_info['availableBalance'])
        if balance > 0:
            print(f"✅ Account found (Balance: {balance} USDC)")
        else:
            print("Depositing...")
            if not await deposit_indirect(l1_address):
                return
            await asyncio.sleep(30)
            account_info = await wait_for_account(l1_address)
            if not account_info:
                print("❌ Account not found after deposit")
                return
    else:
        print("Depositing to create account...")
        if not await deposit_indirect(l1_address):
            return
        account_info = await wait_for_account(l1_address)
        if not account_info:
            print("❌ Account not found after deposit")
            return
    
    print(f"✅ Account: {account_info['accountIndex']}, Balance: {account_info['availableBalance']} USDC")
    
    private_keys, public_keys = await generate_api_keys(account_info["accountIndex"])
    await register_api_keys(account_info["accountIndex"], private_keys, public_keys)
    
    save_config(str(account_info["accountIndex"]), l1_address, account_info["l2Address"], private_keys)
    
    print(f"\n✅ Onboarding complete")
    print(f"   Config: {OUTPUT_FILE}")


if __name__ == "__main__":
    asyncio.run(main())

