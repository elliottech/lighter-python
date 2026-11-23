import unittest

from eth_account import Account
from eth_account.messages import encode_defunct

from lighter.signer_client import api_key_restrictions_json, build_api_key_restrictions_message


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
        account = Account.from_key("0x" + "12345678" * 8)
        message = build_api_key_restrictions_message(1, 4, "ab", "[]", "[]", "[]", 0, 1, 304)
        signature = account.sign_message(encode_defunct(text=message))
        recovered = Account.recover_message(encode_defunct(text=message), signature=signature.signature)
        self.assertEqual(recovered, account.address)


if __name__ == "__main__":
    unittest.main()
