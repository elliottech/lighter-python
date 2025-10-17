import os
import asyncio
import lighter
from config import config

# --- Constants ---
BASE_URL = "https://mainnet.zklighter.elliot.ai"

class LighterClient:
    """
    A wrapper for the Lighter SDK to simplify client initialization and access.
    Handles authentication and provides easy access to the various API clients.
    The client must be initialized asynchronously using the `create` class method.
    """
    def __init__(self):
        # Credentials are loaded but clients are not initialized here
        self.eth_private_key = config.get('credentials.eth_private_key')
        self.api_key_private_key = config.get('credentials.api_key_private_key')
        self.account_index = config.get('credentials.account_index')
        self.api_key_index = config.get('credentials.api_key_index')

        self.api_client = None
        self.signer_client = None
        self.account_api = None
        self.order_api = None
        self.transaction_api = None

    @classmethod
    async def create(cls):
        """Asynchronously creates and initializes the LighterClient."""
        self = cls()

        if not all([self.eth_private_key, self.api_key_private_key, self.account_index is not None, self.api_key_index is not None]):
            raise ValueError("Missing one or more required credentials in config.yaml")

        if "YOUR_ETH_PRIVATE_KEY" in self.eth_private_key or "YOUR_LIGHTER_API_PRIVATE_KEY" in self.api_key_private_key:
            print("WARNING: Using default placeholder credentials. Please update config.yaml.")

        # Initialize clients within an async context
        self.api_client = lighter.ApiClient(configuration=lighter.Configuration(host=BASE_URL))
        self.signer_client = lighter.SignerClient(
            url=BASE_URL,
            private_key=self.api_key_private_key,
            account_index=self.account_index,
            api_key_index=self.api_key_index
        )

        self.account_api = lighter.AccountApi(self.api_client)
        self.order_api = lighter.OrderApi(self.api_client)
        self.transaction_api = lighter.TransactionApi(self.api_client)

        return self

    async def get_account_info(self):
        """
        Fetches basic information for the configured account.
        A simple method to test connectivity and authentication.
        """
        if not self.account_api:
            raise Exception("Client not initialized. Please use `await LighterClient.create()`.")

        try:
            account = await self.account_api.account(by="index", value=str(self.account_index))
            return account
        except Exception as e:
            print(f"Error fetching account info: {e}")
            return None

    async def close(self):
        """Closes the aiohttp client session."""
        if self.api_client:
            await self.api_client.close()


# --- Example Usage (for testing) ---
async def main():
    print("--- Initializing Lighter Client ---")
    client = None
    try:
        client = await LighterClient.create()
        print("Client initialized.")

        print("\n--- Fetching Account Info ---")
        account_info = await client.get_account_info()

        if account_info:
            print("Account Info:", account_info)
        else:
            print("Could not fetch account info (this is expected with placeholder keys).")

    except ValueError as e:
        print(f"Initialization failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        if client:
            await client.close()


if __name__ == '__main__':
    asyncio.run(main())