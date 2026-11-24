import unittest
from unittest.mock import AsyncMock, MagicMock, patch

from eth_account import Account
from eth_account.messages import encode_defunct

import lighter
from lighter.signer_client import SignerClient, api_key_restrictions_json, build_api_key_restrictions_message

ETH_PRIVATE_KEY = "0x" + "12345678" * 8


class TestApiKeyRestrictionsMessage(unittest.TestCase):
    def test_message_matches_server_template(self):
        message = build_api_key_restrictions_message(
            account_index=3,
            api_key_index=4,
            public_key="0xABCDEF",
            market_ids=api_key_restrictions_json([0, 1]),
            series=api_key_restrictions_json([{"creator_account_index": 3, "tag": "btc-updown-5m"}]),
            allowed_ips=api_key_restrictions_json(["203.0.113.7"]),
            valid_until=0,
            timestamp=1767139200,
            chain_id=304,
        )
        self.assertEqual(
            message,
            "Set API Key Restrictions\n\n"
            "account index: 0x0000000000000003\n"
            "api key index: 0x0000000000000004\n"
            "pubkey: 0xabcdef\n"
            "market ids: [0,1]\n"
            'series: [{"creator_account_index":3,"tag":"btc-updown-5m"}]\n'
            'allowed ips: ["203.0.113.7"]\n'
            "valid until: 0x0000000000000000\n"
            "timestamp: 0x0000000069546780\n"
            "chainId: 0x0000000000000130\n"
            "Only sign this message for a trusted client!",
        )

    def test_signature_recovers_l1_address(self):
        account = Account.from_key(ETH_PRIVATE_KEY)
        message = build_api_key_restrictions_message(1, 4, "ab", "[]", "[]", "[]", 0, 1, 304)
        signature = account.sign_message(encode_defunct(text=message))
        recovered = Account.recover_message(encode_defunct(text=message), signature=signature.signature)
        self.assertEqual(recovered, account.address)


class TestSetApiKeyRestrictionsRequest(unittest.IsolatedAsyncioTestCase):
    async def test_sends_the_strings_it_signs(self):
        client = SignerClient.__new__(SignerClient)
        client.account_index = 7
        client.chain_id = 304
        client.api_client = MagicMock()
        with patch.object(lighter.AccountApi, "set_api_key_restrictions", new_callable=AsyncMock) as send:
            resp, err = await client.set_api_key_restrictions(
                ETH_PRIVATE_KEY,
                4,
                market_ids=[0, 1],
                series=[{"creator_account_index": 3, "tag": "btc-updown-5m"}],
                allowed_ips=["203.0.113.7"],
                valid_until=1769731200,
                public_key="0xABCD",
                timestamp=1767139200,
            )
        self.assertIsNone(err)
        sent = send.call_args.kwargs
        self.assertEqual(sent["account_index"], 7)
        self.assertEqual(sent["api_key_index"], 4)
        self.assertEqual(sent["public_key"], "abcd")
        self.assertEqual(sent["market_ids"], "[0,1]")
        self.assertEqual(sent["series"], '[{"creator_account_index":3,"tag":"btc-updown-5m"}]')
        self.assertEqual(sent["allowed_ips"], '["203.0.113.7"]')
        self.assertEqual(sent["valid_until"], 1769731200)
        self.assertEqual(sent["timestamp"], 1767139200)

        message = build_api_key_restrictions_message(
            7, 4, sent["public_key"], sent["market_ids"], sent["series"], sent["allowed_ips"],
            sent["valid_until"], sent["timestamp"], 304,
        )
        recovered = Account.recover_message(encode_defunct(text=message), signature=sent["signature"])
        self.assertEqual(recovered, Account.from_key(ETH_PRIVATE_KEY).address)

    async def test_empty_lists_clear_restrictions(self):
        client = SignerClient.__new__(SignerClient)
        client.account_index = 7
        client.chain_id = 304
        client.api_client = MagicMock()
        with patch.object(lighter.AccountApi, "set_api_key_restrictions", new_callable=AsyncMock) as send:
            _, err = await client.set_api_key_restrictions(ETH_PRIVATE_KEY, 4, public_key="ab", timestamp=1)
        self.assertIsNone(err)
        sent = send.call_args.kwargs
        self.assertEqual((sent["market_ids"], sent["series"], sent["allowed_ips"], sent["valid_until"]), ("[]", "[]", "[]", 0))


if __name__ == "__main__":
    unittest.main()
