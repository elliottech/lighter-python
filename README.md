# 🚀 Lighter Protocol Random Trading Bot

A sophisticated automated trading bot for the [Lighter Protocol](https://lighter.xyz/) with percentage-based position sizing and intelligent risk management.

## ⚠️ **IMPORTANT DISCLAIMER**

**This software is for educational purposes only. Automated trading involves significant financial risk. Use at your own risk.**

## ✨ Key Features

- **Percentage-based position sizing** - Risk management based on account balance
- **Single position mode** - Hold one position at a time
- **Automatic position closing** - Configurable hold duration
- **Multi-pair trading** - BTC, ETH, HYPE, SOL, BNB support
- **Proxy support** - Route traffic through proxy servers
- **Comprehensive logging** - Detailed trade tracking

## 🛠️ Quick Start

### 1. Installation
```bash
git clone https://github.com/yourusername/lighter-trading-bot.git
cd lighter-trading-bot
pip install -r trading_bot_requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp env.example .env

# Edit with your Lighter API credentials
nano .env
```

### 3. Run the Bot
```bash
# Start bot
python3 start_bot.py start

# Check status
python3 start_bot.py status

# Stop bot
python3 start_bot.py stop
```

## ⚙️ Configuration

Key settings in `.env`:
- `ACCOUNT_BALANCE=500` - Your account balance
- `MIN_POSITION_PERCENT=50` - Minimum risk per trade
- `MAX_POSITION_PERCENT=80` - Maximum risk per trade
- `POSITION_HOLD_MINUTES=5` - How long to hold positions

## 📊 How It Works

1. **Random Selection**: Picks random trading pair and direction
2. **Smart Sizing**: Calculates position size based on account percentage
3. **Order Execution**: Places market order with verification
4. **Position Hold**: Holds for configured duration
5. **Auto Close**: Closes position and repeats cycle

## 🔒 Security

- Environment variables for sensitive data
- Automatic gitignore for credentials
- Process locking prevents multiple instances
- Comprehensive input validation

## 📈 Example Results

```
INFO - Percentage calculation: 67.9% of $500 = $339.60 risk → $1697.98 notional
INFO - Placing SHORT market order: ETH size=0.097 units
INFO - Trade successful! Position opened: ETH SHORT
```

## 🛡️ Risk Management

- Position size capped at 80% of account balance
- Daily trade limits
- Order fill verification
- Single position mode to limit exposure

## 📚 Documentation

- [Lighter Protocol API](https://apidocs.lighter.xyz/reference/status)
- [Setup Guide](SETUP.md)
- [Configuration Reference](CONFIG.md)

## ⚠️ Warning

**CRYPTOCURRENCY TRADING IS HIGHLY RISKY**
- Can lose money quickly
- Never invest more than you can afford to lose
- Test with small amounts first
- Consider this experimental software

---

**Use responsibly and happy trading! 🚀**
