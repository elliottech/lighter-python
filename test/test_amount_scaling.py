import asyncio
import types
import unittest

from lighter.signer_client import SignerClient


def _capture_withdraw_amount(asset_id, amount):
    captured = {}

    def sign_withdraw(asset_index, route_type, amount, skip_nonce, nonce, api_key_index):
        captured["amount"] = amount
        return None, None, None, "stop"

    fake = types.SimpleNamespace(
        ASSET_TO_TICKER_SCALE=SignerClient.ASSET_TO_TICKER_SCALE,
        sign_withdraw=sign_withdraw,
    )
    asyncio.run(SignerClient.withdraw(fake, asset_id, SignerClient.ROUTE_PERP, amount, nonce=1, api_key_index=0))
    return captured["amount"]


class TestAmountScaling(unittest.TestCase):
    def test_withdraw_usdc_amount_is_exact(self):
        # 2.01 * 1e6 == 2009999.9999999998 in binary floating point
        self.assertEqual(_capture_withdraw_amount(SignerClient.ASSET_ID_USDC, 2.01), 2_010_000)

    def test_withdraw_eth_amount_is_exact(self):
        # 0.29 * 1e8 == 28999999.999999996 in binary floating point
        self.assertEqual(_capture_withdraw_amount(SignerClient.ASSET_ID_ETH, 0.29), 29_000_000)

    def test_sub_tick_precision_is_still_truncated(self):
        self.assertEqual(_capture_withdraw_amount(SignerClient.ASSET_ID_USDC, 1.0000009), 1_000_000)


if __name__ == "__main__":
    unittest.main()
