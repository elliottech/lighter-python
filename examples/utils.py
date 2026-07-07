from typing import Tuple, Optional
import logging
import json
import websockets
import lighter


def trim_exception(e: Exception) -> str:
    return str(e).strip().split("\n")[-1]


def save_api_key_config(endpoint_profile, account_index, private_keys, config_file="./api_key_config.json"):
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump({
            "endpointProfile": endpoint_profile.name,
            "accountIndex": account_index,
            "privateKeys": private_keys,
        }, f, ensure_ascii=False, indent=2)


def get_api_key_config(config_file="./api_key_config.json"):
    with open(config_file) as f:
        cfg = json.load(f)

    private_keys_original = cfg["privateKeys"]
    private_key = {}
    for key in private_keys_original.keys():
        private_key[int(key)] = private_keys_original[key]

    profile_name = cfg.get("endpointProfile")
    if profile_name:
        profile = lighter.get_endpoint_profile(profile_name)
    else:
        # Backward compat: build a profile from the raw baseUrl
        base_url = cfg["baseUrl"]
        profile = lighter.EndpointProfile(
            name="custom",
            api_url=base_url,
            ws_url=base_url.replace("https", "wss") + "/stream",
            chain_id=304 if ("mainnet" in base_url) else 466324 if ("api.rh.lighter" in base_url) else 300,
        )

    return profile, cfg["accountIndex"], private_key


def default_example_setup(config_file="./api_key_config.json",nonce_management_type=lighter.nonce_manager.NonceManagerType.OPTIMISTIC,endpoint_profile=None,) -> Optional[Tuple[lighter.SignerClient, lighter.ApiClient, websockets.connect]]:
    logging.basicConfig(level=logging.DEBUG)

    config_endpoint, account_index, private_keys = get_api_key_config(config_file)

    profile = endpoint_profile or config_endpoint

    api_url = profile.api_url
    chain_id = profile.chain_id
    ws_url = profile.ws_url

    api_client = lighter.ApiClient(
        configuration=lighter.Configuration(host=api_url)
    )

    client = lighter.SignerClient(
        url=api_url,
        account_index=account_index,
        api_private_keys=private_keys,
        nonce_management_type=nonce_management_type,
        chain_id=chain_id,
    )

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {trim_exception(err)}")
        return None

    return client, api_client, websockets.connect(ws_url)

async def ws_ping(ws_client: websockets.ClientConnection):
    await ws_client.send(json.dumps({"type": "pong"}))

async def ws_subscribe(ws_client: websockets.ClientConnection, channel: str, auth: Optional[str] = None):
    if auth is None:
        await ws_client.send(json.dumps({"type": "subscribe", "channel": channel}))
    else:
        await ws_client.send(json.dumps({"type": "subscribe", "channel": channel, "auth": auth}))

async def ws_send_tx(ws_client: websockets.ClientConnection, tx_type, tx_info, tx_hash):
    # Note: you have the TX Hash from signing the TX
    # You can use this TX Hash to check the status of the TX later on
    # if the server generates a different hash, the signature will fail, so the hash will always be correct
    # because of this, the hash returned by the server will always be the same
    await ws_client.send(
        json.dumps(
            {
                "type": "jsonapi/sendtx",
                "data": {
                    "id": f"my_random_id_{12345678}",  # optional helps id the response
                    "tx_type": tx_type,
                    "tx_info": json.loads(tx_info),
                },
            }
        )
    )

    print(f"expectedHash {tx_hash} response {await ws_client.recv()}")


async def ws_send_batch_tx(ws_client: websockets.ClientConnection, tx_types, tx_infos, tx_hashes):
    # Note: you have the TX Hash from signing the TX
    # You can use this TX Hash to check the status of the TX later on
    # if the server generates a different hash, the signature will fail, so the hash will always be correct
    # because of this, the hash returned by the server will always be the same
    await ws_client.send(
        json.dumps(
            {
                "type": "jsonapi/sendtxbatch",
                "data": {
                    "id": f"my_random_id_{12345678}",  # optional helps id the response
                    "tx_types": json.dumps(tx_types),
                    "tx_infos": json.dumps(tx_infos),
                },
            }
        )
    )

    print(f"expectedHash {tx_hashes} response {await ws_client.recv()}")
