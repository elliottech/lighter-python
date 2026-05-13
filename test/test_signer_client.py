import unittest
from unittest.mock import Mock, patch

import lighter.signer_client as signer_client


class TestSignerLoader(unittest.TestCase):
    def test_initialize_signer_uses_shared_library_path_by_default(self):
        signer = Mock()
        source_library_path = "/signers/signer-arm64.dylib"

        with patch.object(signer_client, "_get_signer_library_path", return_value=source_library_path):
            with patch.object(signer_client, "_load_signer_library", return_value=signer) as load_signer:
                loaded = signer_client._initialize_signer()

        self.assertIs(loaded, signer)
        load_signer.assert_called_once_with(source_library_path)

    def test_initialize_signer_copies_library_when_isolated(self):
        signer = Mock()
        source_library_path = "/signers/signer-arm64.dylib"
        temp_dir = "/tmp/lighter-signer-test"
        isolated_library_path = f"{temp_dir}/signer-arm64.dylib"

        with patch.object(signer_client, "_isolated_signer_directories", []):
            with patch.object(signer_client, "_get_signer_library_path", return_value=source_library_path):
                with patch.object(signer_client.tempfile, "mkdtemp", return_value=temp_dir):
                    with patch.object(signer_client.shutil, "copy2") as copy2:
                        with patch.object(signer_client, "_load_signer_library", return_value=signer) as load_signer:
                            loaded = signer_client._initialize_signer(isolated=True)

        self.assertIs(loaded, signer)
        copy2.assert_called_once_with(source_library_path, isolated_library_path)
        load_signer.assert_called_once_with(isolated_library_path)


class TestSignerClientInit(unittest.TestCase):
    def test_init_defaults_to_isolated_signer_instance(self):
        signer = Mock()
        nonce_manager = Mock()

        with patch.object(signer_client, "_initialize_signer", return_value=signer) as initialize_signer:
            with patch.object(signer_client.lighter, "ApiClient", return_value=Mock()):
                with patch.object(signer_client.lighter, "TransactionApi", return_value=Mock()):
                    with patch.object(signer_client.lighter, "OrderApi", return_value=Mock()):
                        with patch.object(signer_client.nonce_manager, "nonce_manager_factory", return_value=nonce_manager):
                            with patch.object(signer_client.SignerClient, "create_client"):
                                client = signer_client.SignerClient(
                                    url="https://api.testnet.example",
                                    private_key="abc123",
                                    api_key_index=3,
                                    account_index=7,
                                )

        self.assertIs(client.signer, signer)
        initialize_signer.assert_called_once_with(isolated=True)

    def test_init_can_request_isolated_signer_instance(self):
        signer = Mock()
        nonce_manager = Mock()

        with patch.object(signer_client, "_initialize_signer", return_value=signer) as initialize_signer:
            with patch.object(signer_client.lighter, "ApiClient", return_value=Mock()):
                with patch.object(signer_client.lighter, "TransactionApi", return_value=Mock()):
                    with patch.object(signer_client.lighter, "OrderApi", return_value=Mock()):
                        with patch.object(signer_client.nonce_manager, "nonce_manager_factory", return_value=nonce_manager):
                            with patch.object(signer_client.SignerClient, "create_client"):
                                client = signer_client.SignerClient(
                                    url="https://api.testnet.example",
                                    private_key="abc123",
                                    api_key_index=3,
                                    account_index=7,
                                    isolated_signer_instance=True,
                                )

        self.assertIs(client.signer, signer)
        initialize_signer.assert_called_once_with(isolated=True)

    def test_init_can_explicitly_request_shared_signer_instance(self):
        signer = Mock()
        nonce_manager = Mock()

        with patch.object(signer_client, "_initialize_signer", return_value=signer) as initialize_signer:
            with patch.object(signer_client.lighter, "ApiClient", return_value=Mock()):
                with patch.object(signer_client.lighter, "TransactionApi", return_value=Mock()):
                    with patch.object(signer_client.lighter, "OrderApi", return_value=Mock()):
                        with patch.object(signer_client.nonce_manager, "nonce_manager_factory", return_value=nonce_manager):
                            with patch.object(signer_client.SignerClient, "create_client"):
                                client = signer_client.SignerClient(
                                    url="https://api.testnet.example",
                                    private_key="abc123",
                                    api_key_index=3,
                                    account_index=7,
                                    isolated_signer_instance=False,
                                )

        self.assertIs(client.signer, signer)
        initialize_signer.assert_called_once_with(isolated=False)


if __name__ == "__main__":
    unittest.main()
