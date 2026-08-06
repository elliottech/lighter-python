import ctypes
import unittest
from unittest import mock

from lighter import signer_client


class TestSignerMemoryManagement(unittest.TestCase):
    def test_decode_and_free_releases_pointer_once(self):
        value = ctypes.create_string_buffer(b"lighter")
        pointer = ctypes.addressof(value)
        native_free = mock.Mock()

        with mock.patch.object(signer_client, "__native_free", native_free):
            self.assertEqual(signer_client.decode_and_free(pointer), "lighter")

        native_free.assert_called_once_with(pointer)

    def test_decode_and_free_releases_pointer_when_decoding_fails(self):
        value = ctypes.create_string_buffer(b"\xff")
        pointer = ctypes.addressof(value)
        native_free = mock.Mock()

        with mock.patch.object(signer_client, "__native_free", native_free):
            with self.assertRaises(UnicodeDecodeError):
                signer_client.decode_and_free(pointer)

        native_free.assert_called_once_with(pointer)

    def test_free_pointer_ignores_null(self):
        native_free = mock.Mock()

        with mock.patch.object(signer_client, "__native_free", native_free):
            signer_client.free_pointer(None)

        native_free.assert_not_called()

    def test_windows_uses_signer_allocator(self):
        signer = mock.Mock()
        with mock.patch.object(signer_client, "__native_free", None):
            with mock.patch.object(signer_client.os, "name", "nt"):
                with mock.patch.object(
                        signer_client, "get_signer", return_value=signer):
                    native_free = getattr(
                        signer_client, "__get_native_free")()

        self.assertIs(native_free, signer.Free)

    def test_posix_falls_back_when_process_allocator_is_unavailable(self):
        signer = mock.Mock()
        with mock.patch.object(signer_client, "__native_free", None):
            with mock.patch.object(signer_client.os, "name", "posix"):
                with mock.patch.object(
                        signer_client.ctypes, "CDLL", side_effect=OSError):
                    with mock.patch.object(
                            signer_client, "get_signer", return_value=signer):
                        native_free = getattr(
                            signer_client, "__get_native_free")()

        self.assertIs(native_free, signer.Free)


if __name__ == "__main__":
    unittest.main()
