# lighter/endpoint_profiles.py

from dataclasses import dataclass


def normalize_base_url(url: str) -> str:
    return url.rstrip("/")


def join_url(base_url: str, path: str) -> str:
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


@dataclass(frozen=True)
class EndpointProfile:
    name: str
    api_url: str
    ws_url: str
    chain_id: int

    def __post_init__(self):
        object.__setattr__(self, "api_url", normalize_base_url(self.api_url))
        object.__setattr__(self, "ws_url", normalize_base_url(self.ws_url))


MAINNET = EndpointProfile(
    name="mainnet",
    api_url="https://mainnet.zklighter.elliot.ai",
    ws_url="wss://mainnet.zklighter.elliot.ai/stream",
    chain_id=304,
)

TESTNET = EndpointProfile(
    name="testnet",
    api_url="https://testnet.zklighter.elliot.ai",
    ws_url="wss://testnet.zklighter.elliot.ai/stream",
    chain_id=300,
)

ROBINHOOD = EndpointProfile(
    name="robinhood",
    api_url="https://api.rh.lighter.xyz",
    ws_url="wss://api.rh.lighter.xyz/stream",
    chain_id=466324,
)


ROBINHOOD_TESTNET = EndpointProfile(
    name="robinhood_testnet",
    api_url="https://api.rh-testnet.lighter.xyz",
    ws_url="wss://api.rh-testnet.lighter.xyz/stream",
    chain_id=300,
)

DEFAULT_ENDPOINT_PROFILE = MAINNET

ENDPOINT_PROFILES = {
    MAINNET.name: MAINNET,
    ROBINHOOD.name: ROBINHOOD,
    TESTNET.name: TESTNET,
    ROBINHOOD_TESTNET.name: ROBINHOOD_TESTNET,
}


def get_endpoint_profile(name: str) -> EndpointProfile:
    try:
        return ENDPOINT_PROFILES[name]
    except KeyError as exc:
        raise ValueError(f"Unknown endpoint profile: {name}") from exc

def construct_endpoint_profile(name: str, api_url: str, ws_url: str, chain_id: int) -> EndpointProfile:
    return EndpointProfile(name, api_url, ws_url, chain_id)