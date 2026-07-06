# coding: utf-8

import asyncio
import random
import unittest
from types import SimpleNamespace
from unittest import mock

from lighter.errors import ValidationError
from lighter.exceptions import BadRequestException
from lighter.nonce_manager import (
    ApiNonceManager,
    NoOpNonceManager,
    NonceManagerType,
    OptimisticNonceManager,
    nonce_manager_factory,
)
from lighter.signer_client import CODE_OK, process_api_key_and_nonce


def make_manager(manager_cls=OptimisticNonceManager, api_keys=(1,), start_nonce=100):
    api_client = mock.Mock()
    manager = manager_cls(account_index=7, api_client=api_client, api_keys_list=list(api_keys))
    counters = {}

    async def fetch(api_key):
        counters[api_key] = counters.get(api_key, 0) + 1
        return start_nonce

    manager._fetch_nonce = mock.AsyncMock(side_effect=fetch)
    return manager, counters


class DummySigner:
    """Minimal stand-in for SignerClient to exercise process_api_key_and_nonce."""

    def __init__(self, manager):
        self.nonce_manager = manager
        self.sent = []
        self.in_flight = 0
        self.max_in_flight = 0

    @process_api_key_and_nonce
    async def send(self, delay=0.0, fail=False, exc=None, nonce=-1, api_key_index=255):
        self.in_flight += 1
        self.max_in_flight = max(self.max_in_flight, self.in_flight)
        try:
            if delay:
                await asyncio.sleep(delay)
            if exc is not None:
                raise exc
            self.sent.append((api_key_index, nonce))
            if fail:
                return None, SimpleNamespace(code=400), "boom"
            return "tx", SimpleNamespace(code=CODE_OK), None
        finally:
            self.in_flight -= 1


class TestConstructionIsIOFree(unittest.TestCase):
    def test_no_network_on_construction(self):
        with mock.patch("lighter.nonce_manager.requests.get") as sync_get, \
                mock.patch("lighter.nonce_manager.TransactionApi") as tx_api:
            for manager_type in NonceManagerType:
                nonce_manager_factory(
                    nonce_manager_type=manager_type,
                    account_index=1,
                    api_client=mock.Mock(),
                    api_keys_list=[2, 4],
                )
            sync_get.assert_not_called()
            tx_api.assert_not_called()

    def test_empty_api_keys_rejected(self):
        with self.assertRaises(ValidationError):
            OptimisticNonceManager(account_index=1, api_client=mock.Mock(), api_keys_list=[])

    def test_factory_rejects_invalid_type(self):
        with self.assertRaises(ValidationError):
            nonce_manager_factory("bogus", 1, mock.Mock(), [2])


class TestOptimisticNonceManager(unittest.IsolatedAsyncioTestCase):
    async def test_lazy_fetch_happens_once_per_key(self):
        manager, counters = make_manager(api_keys=(3,), start_nonce=100)
        key, nonce = await manager.async_next_nonce(3)
        self.assertEqual((key, nonce), (3, 100))
        key, nonce = await manager.async_next_nonce(3)
        self.assertEqual((key, nonce), (3, 101))
        self.assertEqual(counters[3], 1)

    async def test_rotation_across_keys(self):
        manager, counters = make_manager(api_keys=(1, 2), start_nonce=50)
        first = await manager.async_next_nonce()
        second = await manager.async_next_nonce()
        third = await manager.async_next_nonce()
        self.assertEqual(first, (2, 50))
        self.assertEqual(second, (1, 50))
        self.assertEqual(third, (2, 51))
        self.assertEqual(counters, {1: 1, 2: 1})

    async def test_unknown_api_key_rejected(self):
        manager, _ = make_manager(api_keys=(1,))
        with self.assertRaises(ValidationError):
            await manager.async_next_nonce(9)
        with self.assertRaises(ValidationError):
            manager.next_nonce(9)

    async def test_acknowledge_failure_reuses_nonce(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=10)
        _, nonce = await manager.async_next_nonce(1)
        manager.acknowledge_failure(1)
        _, nonce_again = await manager.async_next_nonce(1)
        self.assertEqual(nonce, nonce_again)

    async def test_acknowledge_failure_before_first_use_is_safe(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=10)
        manager.acknowledge_failure(1)  # must not raise
        _, nonce = await manager.async_next_nonce(1)
        self.assertEqual(nonce, 10)

    async def test_async_hard_refresh_resets_to_server_value(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=10)
        await manager.async_next_nonce(1)
        await manager.async_next_nonce(1)
        manager._fetch_nonce = mock.AsyncMock(return_value=42)
        await manager.async_hard_refresh_nonce(1)
        _, nonce = await manager.async_next_nonce(1)
        self.assertEqual(nonce, 42)

    def test_sync_lazy_fetch(self):
        manager = OptimisticNonceManager(account_index=7, api_client=mock.Mock(), api_keys_list=[1])
        with mock.patch("lighter.nonce_manager.get_nonce_from_api", return_value=20) as sync_get:
            self.assertEqual(manager.next_nonce(1), (1, 20))
            self.assertEqual(manager.next_nonce(1), (1, 21))
            sync_get.assert_called_once()


class TestApiNonceManager(unittest.IsolatedAsyncioTestCase):
    async def test_refreshes_on_every_call(self):
        manager, counters = make_manager(ApiNonceManager, api_keys=(1,), start_nonce=30)
        self.assertEqual(await manager.async_next_nonce(1), (1, 30))
        self.assertEqual(await manager.async_next_nonce(1), (1, 30))
        self.assertEqual(counters[1], 2)

    async def test_rotation(self):
        manager, _ = make_manager(ApiNonceManager, api_keys=(1, 2), start_nonce=30)
        self.assertEqual((await manager.async_next_nonce())[0], 2)
        self.assertEqual((await manager.async_next_nonce())[0], 1)


class TestNoOpNonceManager(unittest.IsolatedAsyncioTestCase):
    async def test_next_nonce_raises(self):
        manager = NoOpNonceManager(account_index=1, api_client=mock.Mock(), api_keys_list=[1])
        with self.assertRaises(ValidationError):
            manager.next_nonce()
        with self.assertRaises(ValidationError):
            await manager.async_next_nonce()

    async def test_refresh_and_failure_are_noops(self):
        manager = NoOpNonceManager(account_index=1, api_client=mock.Mock(), api_keys_list=[1])
        manager.acknowledge_failure(1)
        manager.refresh_nonce(1)
        manager.hard_refresh_nonce(1)
        await manager.async_refresh_nonce(1)
        await manager.async_hard_refresh_nonce(1)
        self.assertEqual(manager.nonce, {})


class TestProcessApiKeyAndNonce(unittest.IsolatedAsyncioTestCase):
    async def test_single_key_concurrent_sends_are_ordered(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        random.seed(1234)
        results = await asyncio.gather(
            *[signer.send(delay=random.uniform(0.0, 0.02)) for _ in range(20)]
        )
        for _, ret, err in results:
            self.assertIsNone(err)
            self.assertEqual(ret.code, CODE_OK)
        nonces = [nonce for _, nonce in signer.sent]
        self.assertEqual(nonces, sorted(nonces))
        self.assertEqual(len(set(nonces)), 20)
        self.assertEqual(nonces, list(range(0, 20)))

    async def test_multiple_keys_send_in_parallel(self):
        manager, _ = make_manager(api_keys=(1, 2), start_nonce=0)
        signer = DummySigner(manager)
        await asyncio.gather(*[signer.send(delay=0.05) for _ in range(2)])
        self.assertEqual(signer.max_in_flight, 2)
        self.assertEqual({key for key, _ in signer.sent}, {1, 2})

    async def test_same_key_sends_are_serialized(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        await asyncio.gather(*[signer.send(delay=0.02) for _ in range(3)])
        self.assertEqual(signer.max_in_flight, 1)

    async def test_failure_return_code_reuses_nonce(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        await signer.send(fail=True)
        await signer.send()
        nonces = [nonce for _, nonce in signer.sent]
        self.assertEqual(nonces, [0, 0])

    async def test_invalid_nonce_triggers_async_hard_refresh(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=0)
        # first fetch initializes lazily (10), second fetch is the hard refresh (42)
        manager._fetch_nonce = mock.AsyncMock(side_effect=[10, 42])
        signer = DummySigner(manager)
        exc = BadRequestException(status=400, reason="invalid nonce")
        created_tx, ret, err = await signer.send(exc=exc)
        self.assertIsNone(created_tx)
        self.assertIsNone(ret)
        self.assertIn("invalid nonce", err)
        self.assertEqual(manager._fetch_nonce.await_count, 2)
        await signer.send()
        self.assertEqual(signer.sent, [(1, 42)])

    async def test_other_bad_request_acknowledges_failure(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        exc = BadRequestException(status=400, reason="insufficient balance")
        _, _, err = await signer.send(exc=exc)
        self.assertIn("insufficient balance", err)
        await signer.send()
        self.assertEqual(signer.sent, [(1, 0)])  # failed nonce is reused

    async def test_non_bad_request_exception_propagates(self):
        manager, _ = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        with self.assertRaises(RuntimeError):
            await signer.send(exc=RuntimeError("boom"))

    async def test_explicit_nonce_bypasses_manager(self):
        manager, counters = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        created_tx, ret, err = await signer.send(nonce=7, api_key_index=3)
        self.assertIsNone(err)
        self.assertEqual(signer.sent, [(3, 7)])
        self.assertEqual(counters, {})
        self.assertEqual(manager.nonce, {})

    async def test_explicit_nonce_bad_request_returns_error_without_touching_manager(self):
        manager, counters = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        exc = BadRequestException(status=400, reason="invalid nonce")
        created_tx, ret, err = await signer.send(nonce=7, api_key_index=3, exc=exc)
        self.assertIsNone(created_tx)
        self.assertIsNone(ret)
        self.assertIn("invalid nonce", err)
        self.assertEqual(counters, {})
        self.assertEqual(manager.nonce, {})

    async def test_noop_manager_requires_explicit_nonce(self):
        manager = NoOpNonceManager(account_index=1, api_client=mock.Mock(), api_keys_list=[1])
        signer = DummySigner(manager)
        with self.assertRaises(ValidationError):
            await signer.send()
        created_tx, ret, err = await signer.send(nonce=5, api_key_index=1)
        self.assertIsNone(err)
        self.assertEqual(signer.sent, [(1, 5)])

    async def test_concurrent_first_use_fetches_once(self):
        manager, counters = make_manager(api_keys=(1,), start_nonce=0)
        signer = DummySigner(manager)
        await asyncio.gather(*[signer.send() for _ in range(5)])
        self.assertEqual(counters[1], 1)
        nonces = [nonce for _, nonce in signer.sent]
        self.assertEqual(nonces, list(range(0, 5)))


if __name__ == "__main__":
    unittest.main()
