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

# Constants
ASSET_INDEX_USDC = 3
ROUTE_TYPE_PERP = 0
USDC_CONTRACT = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
ZKLIGHTER_CONTRACT = "0x3B4D794a66304F130a4Db8F2551B0070dfCf5ca7"

# Environment variables
BASE_URL = os.getenv("BASE_URL", "https://testnet.zklighter.elliot.ai")
ETH_PRIVATE_KEY = os.getenv("ETH_PRIVATE_KEY", "")
L1_RPC_URL = os.getenv("L1_RPC_URL", "")
DEPOSIT_AMOUNT = float(os.getenv("DEPOSIT_AMOUNT", "6"))
OUTPUT_FILE = "api_key_config.json"
API_KEY_INDEX = int(os.getenv("API_KEY_INDEX", "4"))
NUM_API_KEYS = int(os.getenv("NUM_API_KEYS", "1"))

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


def deposit_direct(deposit_to_address: str) -> bool:
    """
    Direct deposit via Ethereum using deposit(address _to, uint16 _assetIndex, uint8 _routeType, uint256 _amount).
    Method ID: 0x8a857083
    """
    account = Account.from_key(ETH_PRIVATE_KEY)
    wallet_address = to_checksum_address(account.address)
    deposit_to_address = to_checksum_address(deposit_to_address)
    usdc_address = to_checksum_address(USDC_CONTRACT)
    zklighter_address = to_checksum_address(ZKLIGHTER_CONTRACT)
    
    decimals_selector = '0x313ce567'
    resp = requests.post(L1_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_address, "data": decimals_selector}, "latest"],
        "id": 1
    })
    decimals = int(resp.json()["result"], 16)
    amount_in_units = int(DEPOSIT_AMOUNT * (10 ** decimals))
    
    balance_selector = '0x70a08231'
    balance_data = balance_selector + wallet_address[2:].rjust(64, '0')
    resp = requests.post(L1_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_address, "data": balance_data}, "latest"],
        "id": 1
    })
    balance = int(resp.json()["result"], 16)
    if balance < amount_in_units:
        print(f"❌ Insufficient balance. Required: {DEPOSIT_AMOUNT} USDC")
        return False
    
    allowance_selector = '0xdd62ed3e'
    allowance_data = allowance_selector + encode(['address', 'address'], [wallet_address, zklighter_address]).hex()
    resp = requests.post(L1_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_call",
        "params": [{"to": usdc_address, "data": allowance_data}, "latest"],
        "id": 1
    })
    allowance = int(resp.json()["result"], 16)
    
    resp = requests.post(L1_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_getTransactionCount",
        "params": [wallet_address, "latest"],
        "id": 1
    })
    nonce = int(resp.json()["result"], 16)
    
    resp = requests.post(L1_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_gasPrice",
        "params": [],
        "id": 1
    })
    gas_price = int(resp.json()["result"], 16)
    
    if allowance < amount_in_units:
        approve_selector = '0x095ea7b3'
        approve_data = approve_selector + encode(['address', 'uint256'], [zklighter_address, amount_in_units]).hex()
        
        tx = {"to": usdc_address, "value": 0, "gas": 100000, "gasPrice": gas_price, "nonce": nonce, "chainId": 1, "data": approve_data}
        signed = account.sign_transaction(tx)
        raw_tx = '0x' + signed.raw_transaction.hex()
        tx_hash = requests.post(L1_RPC_URL, json={
            "jsonrpc": "2.0",
            "method": "eth_sendRawTransaction",
            "params": [raw_tx],
            "id": 1
        }).json().get("result")
        
        if not tx_hash:
            print("❌ Approval failed")
            return False
        
        # Wait for approval confirmation
        for _ in range(30):
            receipt = requests.post(L1_RPC_URL, json={
                "jsonrpc": "2.0",
                "method": "eth_getTransactionReceipt",
                "params": [tx_hash],
                "id": 1
            }).json().get("result")
            if receipt and receipt.get("status") == "0x1":
                break
            time.sleep(2)
        
        resp = requests.post(L1_RPC_URL, json={
            "jsonrpc": "2.0",
            "method": "eth_getTransactionCount",
            "params": [wallet_address, "latest"],
            "id": 1
        })
        nonce = int(resp.json()["result"], 16)
    
    deposit_selector = '0x8a857083'
    deposit_data = deposit_selector + encode(
        ['address', 'uint16', 'uint8', 'uint256'],
        [deposit_to_address, ASSET_INDEX_USDC, ROUTE_TYPE_PERP, amount_in_units]
    ).hex()
    
    tx = {"to": zklighter_address, "value": 0, "gas": 200000, "gasPrice": gas_price, "nonce": nonce, "chainId": 1, "data": deposit_data}
    signed = account.sign_transaction(tx)
    raw_tx = '0x' + signed.raw_transaction.hex()
    
    tx_hash = requests.post(L1_RPC_URL, json={
        "jsonrpc": "2.0",
        "method": "eth_sendRawTransaction",
        "params": [raw_tx],
        "id": 1
    }).json().get("result")
    
    if not tx_hash:
        print("❌ Deposit failed")
        return False
    
    print(f"✅ Deposit tx: {tx_hash}")
    return True


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
    if not ETH_PRIVATE_KEY or not L1_RPC_URL:
        print("❌ ETH_PRIVATE_KEY and L1_RPC_URL required")
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
            deposit_address = account_info.get("l2Address") or l1_address
            if not deposit_direct(deposit_address):
                return
            await asyncio.sleep(30)
            account_info = await wait_for_account(l1_address)
            if not account_info:
                print("❌ Account not found after deposit")
                return
    else:
        print("Depositing to create account...")
        if not deposit_direct(l1_address):
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

