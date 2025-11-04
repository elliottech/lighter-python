import os
from pathlib import Path


# Project root and .secret (see .secret.example) parsing used only for tests
_ROOT = Path(__file__).resolve().parents[1]
_SECRET_PATH = _ROOT / ".secret"

# Default testnet base URL
BASE_URL = "https://testnet.zklighter.elliot.ai"


def _load_secret_file(path: Path) -> dict:
    """Parse KEY=VALUE lines from the repo's .secret for test credentials."""
    secrets: dict = {}
    if not path.exists():
        raise FileNotFoundError(f".secret file not found at: {path}")
    with path.open("r") as fh:
        for raw in fh:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            secrets[key.strip()] = value.strip()
    return secrets


_SECRETS = _load_secret_file(_SECRET_PATH)

# Exported constants used by tests for signing operations
API_KEY_PRIVATE_KEY = _SECRETS["LIGHTER_API_PRIVATE_KEY"]
API_KEY_INDEX = int(_SECRETS["LIGHTER_API_KEY_INDEX"])  
ACCOUNT_INDEX = int(_SECRETS["LIGHTER_ACCOUNT_INDEX"])  
L1_PRIVATE_KEY = _SECRETS.get("LIGHTER_L1_ACCOUNT_PRIVATE_KEY")
API_PUBLIC_KEY = _SECRETS.get("LIGHTER_API_PUBLIC_KEY")

# Default values for integration tests
DEFAULT_MARKET_INDEX = 0
ORDER_BASE_AMOUNT = 1000
SLIPPAGE_TEST_BASE_AMOUNT = 10_000_000_000
DEFAULT_NONCE = 1
