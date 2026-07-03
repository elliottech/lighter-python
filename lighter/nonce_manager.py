import abc
import enum
import json
from typing import Optional, Tuple, List

import requests

from lighter.api_client import ApiClient
from lighter.errors import ValidationError
from urllib.parse import urlencode


def get_nonce_from_api(client: ApiClient, account_index: int, api_key: int) -> int:
    #  uses request to avoid async initialization
    req = requests.get(
        client.configuration.host + "/api/v1/nextNonce",
        params={"account_index": account_index, "api_key_index": api_key},
    )
    if req.status_code != 200:
        raise Exception(f"couldn't get nonce {req.content}")
    return req.json()["nonce"]

async def get_nonce_from_api_async(client: ApiClient, account_index: int, api_key: int) -> int:
    query = urlencode({"account_index": account_index, "api_key_index": api_key})
    resp = await client.rest_client.request(
        "GET",
        f"{client.configuration.host}/api/v1/nextNonce?{query}",
    )
    body = await resp.read()
    if resp.status != 200:
        raise Exception(f"couldn't get nonce {body}")
    return json.loads(body.decode("utf-8"))["nonce"]


class NonceManager(abc.ABC):
    def __init__(
            self,
            account_index: int,
            api_client: ApiClient,
            api_keys_list: List[int],
            fetch_initial_nonce: bool = True,
    ):
        if len(api_keys_list) == 0:
            raise ValidationError(f"No API Key provided")

        self.current = 0  # cycle through api keys
        self.account_index = account_index
        self.api_client = api_client
        self.api_keys_list = api_keys_list
        self.nonce = {}
        if fetch_initial_nonce:
            self.nonce = {
                api_keys_list[i]: get_nonce_from_api(api_client, account_index, api_keys_list[i]) - 1
                for i in range(len(api_keys_list))
            }

    def refresh_nonce(self, api_key: int) -> int:
        self.nonce[api_key] = get_nonce_from_api(self.api_client, self.account_index, api_key)
        return self.nonce[api_key]

    def hard_refresh_nonce(self, api_key: int):
        self.nonce[api_key] = get_nonce_from_api(self.api_client, self.account_index, api_key) - 1

    @abc.abstractmethod
    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        pass

    def acknowledge_failure(self, api_key: int) -> None:
        pass

    async def async_initialize(self):
        self.nonce = {
            api_key: await get_nonce_from_api_async(self.api_client, self.account_index, api_key) - 1
            for api_key in self.api_keys_list
        }

    async def async_refresh_nonce(self, api_key: int) -> int:
        self.nonce[api_key] = await get_nonce_from_api_async(self.api_client, self.account_index, api_key)
        return self.nonce[api_key]

    async def async_hard_refresh_nonce(self, api_key: int):
        self.nonce[api_key] = await get_nonce_from_api_async(self.api_client, self.account_index, api_key) - 1

    async def async_next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        return self.next_nonce(api_key)


class OptimisticNonceManager(NonceManager):
    def __init__(
            self,
            account_index: int,
            api_client: ApiClient,
            api_keys_list: List[int],
            fetch_initial_nonce: bool = True,
    ) -> None:
        super().__init__(account_index, api_client, api_keys_list, fetch_initial_nonce=fetch_initial_nonce)

    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        if api_key is None:
            self.current = (self.current + 1) % len(self.api_keys_list)
            api_key = self.api_keys_list[self.current]

        self.nonce[api_key] += 1
        return api_key, self.nonce[api_key]

    def acknowledge_failure(self, api_key: int) -> None:
        self.nonce[api_key] -= 1


class ApiNonceManager(NonceManager):
    def __init__(
            self,
            account_index: int,
            api_client: ApiClient,
            api_keys_list: List[int],
            fetch_initial_nonce: bool = True,
    ) -> None:
        super().__init__(account_index, api_client, api_keys_list, fetch_initial_nonce=fetch_initial_nonce)

    def next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        """
        It is recommended to wait at least 350ms before using the same api key.
        Please be mindful of your transaction frequency when using this nonce manager.
        predicted_execution_time_ms from the response could give you a tighter bound.
        """
        if api_key is None:
            self.current = (self.current + 1) % len(self.api_keys_list)
            api_key = self.api_keys_list[self.current]

        nonce = self.refresh_nonce(api_key)
        return api_key, nonce

    async def async_next_nonce(self, api_key: Optional[int] = None) -> Tuple[int, int]:
        if api_key is None:
            self.current = (self.current + 1) % len(self.api_keys_list)
            api_key = self.api_keys_list[self.current]

        nonce = await self.async_refresh_nonce(api_key)
        return api_key, nonce


class NoOpNonceManager(NonceManager):
    """For users who provide their own nonces (skip_nonce mode)."""
    # noinspection PyMissingConstructor
    def __init__(self, account_index, api_client, api_keys_list, fetch_initial_nonce: bool = True):
        # Skip super().__init__() to avoid the HTTP call
        self.account_index = account_index
        self.api_client = api_client
        self.api_keys_list = api_keys_list
        self.nonce = {}
        self.current = 0

    def next_nonce(self, api_key=None):
        raise ValidationError(
            "NoOpNonceManager does not manage nonces. "
            "You must provide nonce and api_key_index explicitly."
        )

    def acknowledge_failure(self, api_key):
        pass  # no-op

    def refresh_nonce(self, api_key):
        pass  # no-op

    def hard_refresh_nonce(self, api_key):
        pass  # no-op

    async def async_initialize(self):
        pass

    async def async_refresh_nonce(self, api_key):
        pass

    async def async_hard_refresh_nonce(self, api_key):
        pass

    async def async_next_nonce(self, api_key=None):
        return self.next_nonce(api_key)

class NonceManagerType(enum.Enum):
    OPTIMISTIC = 1
    API = 2
    NONE = 3


def nonce_manager_factory(
        nonce_manager_type: NonceManagerType,
        account_index: int,
        api_client: ApiClient,
        api_keys_list: List[int],
        fetch_initial_nonce: bool = True,
) -> NonceManager:
    if nonce_manager_type == NonceManagerType.OPTIMISTIC:
        return OptimisticNonceManager(
            account_index=account_index,
            api_client=api_client,
            api_keys_list=api_keys_list,
            fetch_initial_nonce=fetch_initial_nonce,
        )
    elif nonce_manager_type == NonceManagerType.API:
        return ApiNonceManager(
            account_index=account_index,
            api_client=api_client,
            api_keys_list=api_keys_list,
            fetch_initial_nonce=fetch_initial_nonce,
        )
    elif nonce_manager_type == NonceManagerType.NONE:
        return NoOpNonceManager(
            account_index=account_index,
            api_client=api_client,
            api_keys_list=api_keys_list,
            fetch_initial_nonce=fetch_initial_nonce,
        )
    raise ValidationError("invalid nonce manager type")
