import asyncio
import logging
import lighter
import requests

logging.basicConfig(level=logging.DEBUG)

BASE_URL = "https://mainnet.zklighter.elliot.ai"

# You can get the values from the system_setup.py script
# API_KEY_PRIVATE_KEY =
# ACCOUNT_INDEX =
# API_KEY_INDEX =


async def main():
    client = lighter.SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE_KEY,
        account_index=ACCOUNT_INDEX,
        api_key_index=API_KEY_INDEX,
    )

    err = client.check_client()
    if err is not None:
        print(f"CheckClient error: {err}")
        return

    auth, err = client.create_auth_token_with_expiry(
        lighter.SignerClient.DEFAULT_10_MIN_AUTH_EXPIRY
    )

    response = requests.post(
        f"{BASE_URL}/api/v1/changeAccountTier",
        data={"account_index": ACCOUNT_INDEX, "new_tier": "premium"},
        headers={"Authorization": auth},
    )
    if response.status_code != 200:
        print(f"Error: {response.text}")
        return
    print(response.json())


if __name__ == "__main__":
    asyncio.run(main())
