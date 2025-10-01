# Configuration Examples

This directory contains example configurations for different trading strategies.

## 📁 Available Examples

### `conservative.env` - Low Risk Trading
- **Risk per trade**: 10-20% of account balance
- **Leverage**: 2-3x maximum
- **Position hold**: 15 minutes
- **Daily trades**: Limited to 20
- **Recommended for**: Beginners, small accounts ($100-$1000)

### `aggressive.env` - High Risk Trading
- **Risk per trade**: 50-80% of account balance  
- **Leverage**: 8-15x
- **Position hold**: 3 minutes (scalping)
- **Daily trades**: Up to 100
- **Recommended for**: Experienced traders, larger accounts ($2000+)

## 🚀 How to Use

1. **Copy your preferred example**:
   ```bash
   cp examples/conservative.env .env
   ```

2. **Edit with your credentials**:
   ```bash
   nano .env
   ```

3. **Replace placeholder values**:
   - `LIGHTER_API_KEY_PRIVATE_KEY`
   - `LIGHTER_ACCOUNT_INDEX`  
   - `LIGHTER_API_KEY_INDEX`

4. **Adjust settings** to match your risk tolerance and account size

## ⚠️ Important Notes

- **Start Conservative**: Even experienced traders should start with conservative settings
- **Test First**: Always test with small amounts initially
- **Monitor Closely**: Watch the bot's performance, especially in the first few hours
- **Adjust Gradually**: Make small adjustments based on performance

## 🎯 Customization Tips

### Position Sizing
- **Small Account (<$500)**: Use 5-15% position sizes
- **Medium Account ($500-$2000)**: Use 10-30% position sizes  
- **Large Account (>$2000)**: Can use 20-50% position sizes

### Leverage Guidelines
- **BTC/ETH**: Generally safer, can use higher leverage
- **Altcoins**: More volatile, use lower leverage
- **New Tokens**: Highest risk, minimal leverage

### Hold Times
- **Scalping**: 1-5 minutes (requires constant monitoring)
- **Short-term**: 5-30 minutes (balanced approach)
- **Medium-term**: 30+ minutes (less frequent trading)

## 🛡️ Risk Management

Remember:
- Never risk more than you can afford to lose
- Start with the smallest position sizes
- Monitor your account balance regularly
- Stop trading if you hit daily loss limits