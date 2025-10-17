import yaml
from pathlib import Path

class Config:
    """
    Handles loading and accessing configuration settings from a YAML file.
    """
    def __init__(self, config_path: Path):
        self.config_path = config_path
        self.settings = self._load_config()

    def _load_config(self) -> dict:
        """Loads the YAML configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            # In a real application, we might want to create a default config
            # or raise a more specific error.
            raise Exception(f"Configuration file not found at: {self.config_path}")
        except yaml.YAMLError as e:
            raise Exception(f"Error parsing configuration file: {e}")

    def get(self, key: str, default=None):
        """
        Retrieves a value from the configuration.
        Uses dot notation for nested keys (e.g., 'credentials.eth_private_key').
        """
        keys = key.split('.')
        value = self.settings
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

# --- Global Configuration Instance ---
# The path is relative to the project root, assuming the bot is run from there.
CONFIG_FILE_PATH = Path(__file__).parent.parent / 'config' / 'config.yaml'
config = Config(CONFIG_FILE_PATH)

# --- Example Usage (for testing) ---
if __name__ == '__main__':
    print("--- Configuration Loaded ---")
    print(f"Symbol: {config.get('trading.symbol')}")
    print(f"ETH Private Key: {config.get('credentials.eth_private_key')}")
    print(f"TP Offsets: {config.get('trading.tp_offsets')}")
    print(f"Non-existent key: {config.get('trading.non_existent_key', 'default_value')}")