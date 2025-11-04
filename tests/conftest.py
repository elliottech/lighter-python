import pytest
import pytest_asyncio

from lighter.signer_client import SignerClient
from tests.constants import BASE_URL, API_KEY_PRIVATE_KEY, API_KEY_INDEX, ACCOUNT_INDEX


def _disable_ssl_verification_for_lighter():
    # Test-only monkeypatch:
    # - Disable TLS verification for aiohttp and requests inside the SDK
    # - Avoid changing library code; keep production defaults intact
    import lighter.signer_client as sc
    from lighter.configuration import Configuration as _BaseCfg
    import lighter.rest as _rest
    import ssl as _ssl

    class _Cfg(_BaseCfg):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.verify_ssl = False

    sc.Configuration = _Cfg  # type: ignore[assignment]

    # Ensure nonce requests also skip verification (used by NonceManager)
    import lighter.nonce_manager as nm
    import requests as _rq

    def _get_nonce_from_api_noverify(client, account_index: int, api_key_index: int) -> int:
        req = _rq.get(
            client.configuration.host + "/api/v1/nextNonce",
            params={"account_index": account_index, "api_key_index": api_key_index},
            verify=False,
        )
        if req.status_code != 200:
            raise Exception(f"couldn't get nonce {req.content}")
        return req.json()["nonce"]

    nm.get_nonce_from_api = _get_nonce_from_api_noverify  # type: ignore[assignment]

    # Make aiohttp use a non-verifying SSL context
    _orig_create_ctx = _rest.ssl.create_default_context

    def _noverify_ctx(*args, **kwargs):
        ctx = _orig_create_ctx(*args, **kwargs)
        ctx.check_hostname = False
        ctx.verify_mode = _ssl.CERT_NONE
        return ctx

    _rest.ssl.create_default_context = _noverify_ctx  # type: ignore[assignment]


@pytest.fixture(scope="session", autouse=True)
def _ssl_noverify():
    """Disable SSL verification in SDK for this test session only."""
    _disable_ssl_verification_for_lighter()


@pytest_asyncio.fixture
async def client():
    """Provides an initialized SignerClient and handles closing it."""
    client = SignerClient(
        url=BASE_URL,
        private_key=API_KEY_PRIVATE_KEY,
        api_key_index=API_KEY_INDEX,
        account_index=ACCOUNT_INDEX,
    )
    yield client
    await client.close()
