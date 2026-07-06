import abc
import asyncio
import enum
from typing import Dict, Optional, Tuple, List

import requests

from lighter.api.transaction_api import TransactionApi
from lighter.api_client import ApiClient
from lighter.errors import ValidationError


def get_nonce_from_api(client: ApiClient, account_index: int, api_key: int) -> int:
    # Blocking fallback for callers using the sync next_nonce()/refresh paths.
    # The async paths never use this; they go through TransactionApi.
    req = requests.get(
        client.configuration.host + "/api/v1/nextNonce",
        params={"account_index": account_index, "api_key_index": api_key},
    )
    if req.status_code != 200:
        raise Exception(f"couldn't get nonce {req.content}")
    return req.json()["nonce"]


class NonceManager(abc.ABC):
    """
    Nonces are fetched lazily on first use per api key, so constructing a
    manager (and therefore a SignerClient) performs no network I/O and is safe
    inside a running event loop.

    next_nonce() may perform a blocking HTTP call on the first use of each api
    key; inside an event loop use async_next_nonce() instead.
    """

    def __init__(
            self,
            account_index: int,
            api_client: ApiClient,
            api_keys_list: List[int],
    ):
        if len(api_keys_list) == 0:
            raise ValidationError(f"No API Key provided")

        self.current = 0  # cycle through api keys
        self.account_index = account_index
        self.api_client = api_client
        self.api_keys_list = api_keys_list
        self.nonce: Dict[int, int] = {}
        # created lazily so they bind to the running loop on older Pythons
        self._locks: Dict[int, asyncio.Lock] = {}

    def rotate_key(self) -> int:
        self.current = (self.current + 1) % len(self.api_keys_list)
        return self.api_keys_list[self.current]

    def lock(self, api_key: int) -> asyncio.Lock:
        lock = self._locks.get(api_key)
        if lock is None:
            lock = self._locks[api_key] = asyncio.Lock()
        return lock

    def _validate_key(self, api_key: int) -> None:
        if api_key not in self.api_keys_list:
            raise ValidationError(f"unknown api key index {api_key}")

    async def _fetch_nonce(self, api_key: int) -> int:
        resp = await TransactionApi(self.api_client).next_nonce(
            account_index=self.account_index, api_key_index=api_key
        )
        return resp.nonce

    def _ensure_nonce_sync(self, api_key: int) -> None:
        if api_key not in self.nonce:
            self.nonce[api_key] = get_nonce_from_api(self.api_client, self.account_index, api_key) - 1

    async def _ensure_nonce(self, api_key: int) -> None:
        if api_key not in self.nonce:
            self.nonce[api_key] = await self._fetch_nonce(api_key) - 1

    def refresh_nonce(self, api_key: int) -> int:
        self.nonce[api_key] = get_nonce_from_api(self.api_client, self.account_index, api_key)
        return self.nonce[api_key]

    def hard_refresh_nonce(self, api_key: int):
        self.nonce[api_key] = get_nonce_from_api(self.api_client, self.account_index, api_key) - 1

    async def async_refresh_nonce(self, api_key: int) -> int:
        self.nonce[api_key] = await self._fetch_nonce(api_key)
        return self.nonce[api_key]

    async def async_hard_refresh_nonce(self, api_key: int):
        self.nonce[api_key] = await self._fetch_nonce(api_key) - 1

    @abc.abstractmethod
    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        pass

    @abc.abstractmethod
    async def async_next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        pass

    def acknowledge_failure(self, api_key: int) -> None:
        pass


class OptimisticNonceManager(NonceManager):
    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        if api_key is None:
            api_key = self.rotate_key()
        self._validate_key(api_key)
        self._ensure_nonce_sync(api_key)
        self.nonce[api_key] += 1
        return api_key, self.nonce[api_key]

    async def async_next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        if api_key is None:
            api_key = self.rotate_key()
        self._validate_key(api_key)
        await self._ensure_nonce(api_key)
        self.nonce[api_key] += 1
        return api_key, self.nonce[api_key]

    def acknowledge_failure(self, api_key: int) -> None:
        if api_key in self.nonce:
            self.nonce[api_key] -= 1


class ApiNonceManager(NonceManager):
    """
    It is recommended to wait at least 350ms before using the same api key.
    Please be mindful of your transaction frequency when using this nonce manager.
    predicted_execution_time_ms from the response could give you a tighter bound.
    """

    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        if api_key is None:
            api_key = self.rotate_key()
        self._validate_key(api_key)
        nonce = self.refresh_nonce(api_key)
        return api_key, nonce

    async def async_next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        if api_key is None:
            api_key = self.rotate_key()
        self._validate_key(api_key)
        nonce = await self.async_refresh_nonce(api_key)
        return api_key, nonce


class NoOpNonceManager(NonceManager):
    """For users who provide their own nonces (skip_nonce mode)."""

    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        raise ValidationError(
            "NoOpNonceManager does not manage nonces. "
            "You must provide nonce and api_key_index explicitly."
        )

    async def async_next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        return self.next_nonce(api_key)

    def acknowledge_failure(self, api_key):
        pass  # no-op

    def refresh_nonce(self, api_key):
        pass  # no-op

    def hard_refresh_nonce(self, api_key):
        pass  # no-op

    async def async_refresh_nonce(self, api_key):
        pass  # no-op

    async def async_hard_refresh_nonce(self, api_key):
        pass  # no-op


class NonceManagerType(enum.Enum):
    OPTIMISTIC = 1
    API = 2
    NONE = 3


def nonce_manager_factory(
        nonce_manager_type: NonceManagerType,
        account_index: int,
        api_client: ApiClient,
        api_keys_list: List[int],
) -> NonceManager:
    if nonce_manager_type == NonceManagerType.OPTIMISTIC:
        return OptimisticNonceManager(
            account_index=account_index,
            api_client=api_client,
            api_keys_list=api_keys_list,
        )
    elif nonce_manager_type == NonceManagerType.API:
        return ApiNonceManager(
            account_index=account_index,
            api_client=api_client,
            api_keys_list=api_keys_list,
        )
    elif nonce_manager_type == NonceManagerType.NONE:
        return NoOpNonceManager(
            account_index=account_index,
            api_client=api_client,
            api_keys_list=api_keys_list,
        )
    raise ValidationError("invalid nonce manager type")
