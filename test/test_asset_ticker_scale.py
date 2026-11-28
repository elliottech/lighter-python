import asyncio
import types
import unittest

from lighter.signer_client import SignerClient


class FakeOrderApi:
    def __init__(self, assets):
        self.assets = assets
        self.calls = 0

    async def asset_details(self):
        self.calls += 1
        return types.SimpleNamespace(
            asset_details=[types.SimpleNamespace(asset_id=asset_id, decimals=decimals) for asset_id, decimals in self.assets]
        )


def make_client(assets):
    client = SignerClient.__new__(SignerClient)
    client.order_api = FakeOrderApi(assets)
    client.signed = []

    def sign_withdraw(asset_index, route_type, amount, skip_nonce, nonce, api_key_index):
        client.signed.append((asset_index, amount))
        return None, None, None, "stop"

    client.sign_withdraw = sign_withdraw
    return client


def withdraw(client, asset_id, amount):
    return asyncio.run(client.withdraw(asset_id, SignerClient.ROUTE_SPOT, amount, nonce=1, api_key_index=0))


class TestAssetTickerScale(unittest.TestCase):
    def test_scale_follows_the_decimals_of_the_connected_deployment(self):
        # api.rh.lighter.xyz lists asset 5 as AMZN with 6 decimals, mainnet lists it as LINK with 8
        client = make_client([(1, 8), (3, 6), (5, 6)])
        withdraw(client, 5, 1.5)
        self.assertEqual(client.signed, [(5, 1_500_000)])

    def test_asset_added_after_the_sdk_release(self):
        # mainnet asset 14 is weETH with 8 decimals
        client = make_client([(3, 6), (14, 8)])
        withdraw(client, 14, 0.25)
        self.assertEqual(client.signed, [(14, 25_000_000)])

    def test_unknown_asset_is_rejected(self):
        client = make_client([(3, 6)])
        with self.assertRaises(ValueError):
            withdraw(client, 99, 1)
        self.assertEqual(client.signed, [])

    def test_asset_details_are_fetched_once(self):
        client = make_client([(3, 6)])
        withdraw(client, 3, 1)
        withdraw(client, 3, 2)
        self.assertEqual(client.signed, [(3, 1_000_000), (3, 2_000_000)])
        self.assertEqual(client.order_api.calls, 1)


if __name__ == "__main__":
    unittest.main()
