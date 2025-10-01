# Lighter Random Trading Bot

A Python program that opens random long/short positions on Lighter mainnet using the lighter-python SDK. This bot randomly selects trading pairs, position directions, and sizes within configured limits.

## ⚠️ IMPORTANT DISCLAIMER

**This bot is for educational and testing purposes only. Automated trading involves significant financial risk. Use at your own risk and ensure you understand the implications of automated trading before running this bot with real funds.**

## Features

- 🎲 **Random Trading**: Randomly selects markets, position directions (long/short), and position sizes
- 📊 **Multiple Markets**: Supports all available trading pairs on Lighter mainnet
- 🛡️ **Risk Management**: Built-in daily trade limits and position size controls
- 📝 **Comprehensive Logging**: Detailed logging of all trades and bot activities
- ⚙️ **Configurable**: Extensive configuration options for trading parameters
- 🔄 **Async Operations**: Efficient async/await implementation for optimal performance

## Prerequisites

- Python 3.8 or higher
- A Lighter account with API keys
- Sufficient balance in your Lighter account for trading

## Installation

1. **Clone or download the lighter-python repository**
   ```bash
   git clone https://github.com/elliottech/lighter-python.git
   cd lighter-python
   ```

2. **Install the SDK and bot dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r trading_bot_requirements.txt
   ```

3. **Set up your configuration**
   ```bash
   cp config.example.py config.py
   ```

4. **Edit config.py with your credentials**
   - Get your API keys from [https://app.lighter.xyz/apikeys](https://app.lighter.xyz/apikeys)
   - Update `API_KEY_PRIVATE_KEY`, `ACCOUNT_INDEX`, and `API_KEY_INDEX`
   - Adjust trading parameters as needed

## Configuration

### Required Settings

```python
# Your Lighter credentials
API_KEY_PRIVATE_KEY = "0x..."  # Your API key private key
ACCOUNT_INDEX = 1              # Your account index
API_KEY_INDEX = 1              # Your API key index
```

### Trading Parameters

```python
# Position sizing
MIN_POSITION_SIZE = 1000       # Minimum position size
MAX_POSITION_SIZE = 10000      # Maximum position size

# Timing
MIN_TRADE_INTERVAL = 30        # Minimum seconds between trades
MAX_TRADE_INTERVAL = 300       # Maximum seconds between trades

# Risk management
MAX_DAILY_TRADES = 50          # Maximum trades per day
ENABLE_RISK_LIMITS = True      # Enable risk controls
```

### Market Filtering

```python
# Exclude specific markets (by market index)
EXCLUDED_MARKETS = [5, 10]     # Don't trade these markets

# Only trade specific markets (empty = all markets)
PREFERRED_MARKETS = [0, 1, 2]  # Only trade these markets
```

## Usage

### Basic Usage

```bash
python random_trading_bot.py
```

### Running with Custom Log Level

```bash
# For debug output
LOG_LEVEL=DEBUG python random_trading_bot.py

# For minimal output
LOG_LEVEL=WARNING python random_trading_bot.py
```

### Stopping the Bot

- Press `Ctrl+C` to gracefully stop the bot
- The bot will complete any pending operations and display final statistics

## How It Works

1. **Initialization**: 
   - Connects to Lighter mainnet
   - Loads available trading markets
   - Validates configuration

2. **Trading Loop**:
   - Randomly selects a trading market
   - Randomly chooses long (buy) or short (sell) position
   - Generates random position size within configured limits
   - Gets current market price with slippage tolerance
   - Places market order
   - Waits random interval before next trade

3. **Risk Management**:
   - Tracks daily trade count
   - Enforces maximum daily trade limits
   - Validates all parameters before trading

## Example Output

```
2024-01-15 10:30:15 - __main__ - INFO - Initializing Lighter Random Trading Bot...
2024-01-15 10:30:16 - __main__ - INFO - Successfully connected to Lighter mainnet
2024-01-15 10:30:17 - __main__ - INFO - Loaded 8 available markets:
2024-01-15 10:30:17 - __main__ - INFO -   0: ETH-USD
2024-01-15 10:30:17 - __main__ - INFO -   1: BTC-USD
2024-01-15 10:30:17 - __main__ - INFO - Starting random trading bot...
2024-01-15 10:30:18 - __main__ - INFO - Generated trade params: ETH-USD LONG size=5500
2024-01-15 10:30:19 - __main__ - INFO - Placing LONG market order: ETH-USD size=5500 price=250000
2024-01-15 10:30:20 - __main__ - INFO - Trade successful! TX: 0xabc123...
2024-01-15 10:30:20 - __main__ - INFO - Waiting 127 seconds until next trade...
```

## Log Files

The bot creates detailed log files (`trading_bot.log` by default) containing:
- All trade attempts and results
- Market data and pricing information
- Error messages and debugging information
- Trading statistics and performance metrics

## Safety Features

- **Daily Trade Limits**: Prevents excessive trading
- **Position Size Limits**: Controls maximum exposure per trade
- **Market Validation**: Ensures markets exist before trading
- **Error Handling**: Graceful handling of API errors and network issues
- **Graceful Shutdown**: Clean shutdown on interruption

## Troubleshooting

### Common Issues

1. **"Client verification failed"**
   - Check your API_KEY_PRIVATE_KEY, ACCOUNT_INDEX, and API_KEY_INDEX
   - Ensure your API key is active on mainnet

2. **"No available markets found"**
   - Check your EXCLUDED_MARKETS and PREFERRED_MARKETS settings
   - Verify network connectivity to Lighter API

3. **"Daily trade limit reached"**
   - The bot has reached MAX_DAILY_TRADES for today
   - Wait until tomorrow or increase the limit

4. **Import errors**
   - Ensure all dependencies are installed: `pip install -r trading_bot_requirements.txt`

### Debug Mode

Run with debug logging for detailed information:

```python
# In config.py
LOG_LEVEL = "DEBUG"
```

## API Rate Limits

The bot includes built-in delays between trades to respect API rate limits. The default configuration should work well for most use cases, but you may need to adjust `MIN_TRADE_INTERVAL` if you encounter rate limiting issues.

## Support

For issues with the lighter-python SDK, please refer to:
- [Official SDK Repository](https://github.com/elliottech/lighter-python)
- [Lighter API Documentation](https://apidocs.lighter.xyz/reference/status)
- [Lighter Protocol Website](https://lighter.xyz)

## License

This trading bot follows the same license as the lighter-python SDK (Apache 2.0).

---

**Remember: Always test with small amounts first and never risk more than you can afford to lose!**
