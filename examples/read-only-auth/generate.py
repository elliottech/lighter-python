import asyncio
import json
import os
import time
import sys
import lighter


def create_auth_token_for_timestamp(signer_client, timestamp, expiry_hours):
    auth_token, error = signer_client.create_auth_token_with_expiry(expiry_hours * 3600, timestamp=timestamp)
    if error is not None:
        raise Exception(f"Failed to create auth token: {error}")
    return auth_token


async def generate_tokens_for_account(account_info, base_url, duration_days):
    account_index = account_info["account_index"]
    
    if "api_key_private_keys" in account_info:
        api_key_private_keys = account_info["api_key_private_keys"]
        api_key_indices = account_info.get("api_key_indices", list(api_key_private_keys.keys()))
        api_key_index = int(api_key_indices[0]) if api_key_indices else int(list(api_key_private_keys.keys())[0])
        api_key_private_key = api_key_private_keys[str(api_key_index)]
    else:
        api_key_private_key = account_info["api_key_private_key"]
        api_key_index = int(account_info["api_key_index"])

    signer_client = lighter.SignerClient(
        url=base_url,
        account_index=account_index,
        api_private_keys={api_key_index: api_key_private_key},
    )

    current_time = int(time.time())
    interval_seconds = 6 * 3600
    start_timestamp = (current_time // interval_seconds) * interval_seconds

    num_tokens = 4 * duration_days
    expiry_hours = 8

    tokens = {}
    for i in range(num_tokens):
        timestamp = start_timestamp + (i * interval_seconds)
        try:
            auth_token = create_auth_token_for_timestamp(signer_client, timestamp, expiry_hours)
            tokens[str(timestamp)] = auth_token
        except Exception as e:
            print(f"Failed to generate token for timestamp {timestamp}: {e}")

    await signer_client.close()

    return account_index, tokens


async def main():
    config_file = "config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"error: config file '{config_file}' not found", file=sys.stderr)
        print("error: run setup.py first: python3 setup.py > config.json", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"error: invalid JSON in config file: {e}", file=sys.stderr)
        sys.exit(1)

    num_days = int(os.getenv("NUM_DAYS") or 28)
    base_url = config.get("BASE_URL")
    accounts = config.get("ACCOUNTS", [])
    duration_days = config.get("DURATION_IN_DAYS", num_days)

    if not base_url:
        print("error: BASE_URL not found in config", file=sys.stderr)
        sys.exit(1)

    if not accounts:
        print("error: no accounts found in config", file=sys.stderr)
        sys.exit(1)

    auth_tokens = {}
    for account_info in accounts:
        account_index, tokens = await generate_tokens_for_account(account_info, base_url, duration_days)
        auth_tokens[str(account_index)] = tokens

    output_file = "auth-tokens.json"
    with open(output_file, "w") as f:
        json.dump(auth_tokens, f, indent=2)

    print(f"Successfully generated tokens and saved to {output_file}")


if __name__ == "__main__":
    asyncio.run(main())
