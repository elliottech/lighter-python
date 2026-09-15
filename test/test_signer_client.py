import ctypes
import concurrent.futures
import struct
import time
import unittest
from unittest import mock

from lighter import signer_client


def pack_batch_record(tx_type, tx_info=b'', tx_hash=b'', error=b''):
    return (
        struct.pack('<B3xIII', tx_type, len(tx_info), len(tx_hash), len(error))
        + tx_info + tx_hash + error
    )


class TestSignerMemoryManagement(unittest.TestCase):
    def test_enables_stack_bound_cache_when_supported(self):
        native = type('Native', (), {})()
        native.FastEnableStackBoundCache = mock.Mock(return_value=1)

        enabled = signer_client._enable_stack_bound_cache(native)

        self.assertTrue(enabled)
        self.assertEqual(native.FastEnableStackBoundCache.argtypes, [])
        self.assertIs(native.FastEnableStackBoundCache.restype, ctypes.c_int)
        native.FastEnableStackBoundCache.assert_called_once_with()

    def test_stack_bound_cache_is_optional(self):
        self.assertFalse(signer_client._enable_stack_bound_cache(object()))

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

    def test_get_signer_publishes_one_fully_initialized_instance(self):
        native = object()

        def populate(_signer):
            time.sleep(0.01)

        with mock.patch.object(signer_client, "__signer", None):
            with mock.patch.object(
                    signer_client, "__get_shared_library",
                    return_value=native) as load:
                with mock.patch.object(
                        signer_client, "__populate_shared_library_functions",
                        side_effect=populate) as populate_mock:
                    with concurrent.futures.ThreadPoolExecutor(
                            max_workers=16) as executor:
                        results = list(executor.map(
                            lambda _: signer_client.get_signer(), range(64)))

        self.assertTrue(all(result is native for result in results))
        load.assert_called_once_with()
        populate_mock.assert_called_once_with(native)


class TestBatchSigning(unittest.TestCase):
    def test_prepare_signer_nonces(self):
        native = mock.Mock()
        native.PrepareSignerNonces.return_value = None
        client = signer_client.SignerClient.__new__(signer_client.SignerClient)
        client.signer = native

        client.prepare_signer_nonces(128)

        native.PrepareSignerNonces.assert_called_once_with(128)

    def test_decode_signed_tx_batch(self):
        packed = (
            struct.pack('<I', 2)
            + pack_batch_record(14, b'{"Nonce":7}', b'hash-7')
            + pack_batch_record(0, error=b'invalid order')
        )

        self.assertEqual(signer_client.decode_signed_tx_batch(packed), [
            (14, '{"Nonce":7}', 'hash-7', None),
            (None, None, None, 'invalid order'),
        ])

    def test_decode_signed_tx_batch_rejects_truncation(self):
        packed = struct.pack('<I', 1) + pack_batch_record(
            14, b'{"Nonce":7}', b'hash-7')[:-1]

        with self.assertRaisesRegex(ValueError, 'truncated payload'):
            signer_client.decode_signed_tx_batch(packed)

    def test_decode_signed_tx_batch_rejects_trailing_data(self):
        packed = struct.pack('<I', 0) + b'extra'

        with self.assertRaisesRegex(ValueError, 'trailing data'):
            signer_client.decode_signed_tx_batch(packed)

    def test_decode_signed_tx_batch_rejects_count_overflow(self):
        packed = struct.pack('<I', 10_001)

        with self.assertRaisesRegex(ValueError, 'count exceeds'):
            signer_client.decode_signed_tx_batch(packed)

    def test_sign_create_orders_batch_decodes_one_allocation(self):
        packed = (
            struct.pack('<I', 2)
            + pack_batch_record(14, b'{"Nonce":10}', b'hash-10')
            + pack_batch_record(14, b'{"Nonce":11}', b'hash-11')
        )

        class FakeSigner:
            def __init__(self):
                self.buffer = ctypes.create_string_buffer(packed)
                self.arguments = None

            def SignCreateOrdersBatch(self, *arguments):
                self.arguments = arguments
                return signer_client.SignedTxBatchResponse(
                    ctypes.addressof(self.buffer), len(packed), None)

        native = FakeSigner()
        client = signer_client.SignerClient.__new__(signer_client.SignerClient)
        client.signer = native
        client.account_index = 42
        orders = [
            signer_client.CreateOrderTxReq(
                MarketIndex=i,
                ClientOrderIndex=100 + i,
                BaseAmount=1_000,
                Price=2_000,
                IsAsk=i,
                Type=0,
                TimeInForce=1,
                ReduceOnly=0,
                TriggerPrice=0,
                OrderExpiry=-1,
            )
            for i in range(2)
        ]

        with mock.patch.object(signer_client, 'free_pointer') as native_free:
            result = client.sign_create_orders_batch(
                orders, 10, api_key_index=3)

        self.assertEqual(result, [
            (14, '{"Nonce":10}', 'hash-10', None),
            (14, '{"Nonce":11}', 'hash-11', None),
        ])
        self.assertEqual(native.arguments[1], 2)
        self.assertEqual(native.arguments[8], 10)
        self.assertEqual(native.arguments[9], 3)
        self.assertEqual(native.arguments[10], 42)
        self.assertEqual(native.arguments[0][1].ClientOrderIndex, 101)
        self.assertEqual(native_free.call_count, 2)

    def test_sign_create_orders_batch_falls_back_for_old_signer(self):
        client = signer_client.SignerClient.__new__(signer_client.SignerClient)
        client.signer = object()
        client.account_index = 42
        orders = [
            signer_client.CreateOrderTxReq(),
            signer_client.CreateOrderTxReq(),
        ]

        with mock.patch.object(
                client,
                'sign_create_order',
                return_value=(14, '{}', 'hash', None)
        ) as sign_one:
            result = client.sign_create_orders_batch(orders, 20)

        self.assertEqual(len(result), 2)
        self.assertEqual(sign_one.call_args_list[0].kwargs['nonce'], 20)
        self.assertEqual(sign_one.call_args_list[1].kwargs['nonce'], 21)

    def test_sign_create_orders_batch_rejects_default_nonce_before_fallback(self):
        client = signer_client.SignerClient.__new__(signer_client.SignerClient)
        client.signer = object()
        orders = [signer_client.CreateOrderTxReq()]

        with mock.patch.object(client, 'sign_create_order') as sign_one:
            with self.assertRaisesRegex(ValueError, 'explicit non-negative'):
                client.sign_create_orders_batch(orders, -1)

        sign_one.assert_not_called()

    def test_sign_create_orders_batch_rejects_nonce_overflow(self):
        client = signer_client.SignerClient.__new__(signer_client.SignerClient)
        client.signer = object()
        orders = [
            signer_client.CreateOrderTxReq(),
            signer_client.CreateOrderTxReq(),
        ]

        with self.assertRaisesRegex(ValueError, 'overflows int64'):
            client.sign_create_orders_batch(orders, (1 << 63) - 1)

    def test_sign_create_orders_batch_rejects_short_native_response(self):
        packed = struct.pack('<I', 1) + pack_batch_record(
            14, b'{"Nonce":10}', b'hash-10')

        class FakeSigner:
            def __init__(self):
                self.buffer = ctypes.create_string_buffer(packed)

            def SignCreateOrdersBatch(self, *_arguments):
                return signer_client.SignedTxBatchResponse(
                    ctypes.addressof(self.buffer), len(packed), None)

        client = signer_client.SignerClient.__new__(signer_client.SignerClient)
        client.signer = FakeSigner()
        client.account_index = 42
        orders = [
            signer_client.CreateOrderTxReq(),
            signer_client.CreateOrderTxReq(),
        ]

        with mock.patch.object(signer_client, 'free_pointer'):
            with self.assertRaisesRegex(
                    RuntimeError, '1 results for 2 orders'):
                client.sign_create_orders_batch(orders, 10)


if __name__ == "__main__":
    unittest.main()
