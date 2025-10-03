# 🕐 Dynamic Position Hold Times

The Lighter Trading Bot now supports **dynamic position hold times** instead of fixed durations! This gives you much more flexibility in your trading strategies.

## 🎯 **Available Hold Time Modes**

### **1. Random Hold Times (Default)**
Bot picks a random duration between min/max for each position.
```env
MIN_POSITION_HOLD_MINUTES=3
MAX_POSITION_HOLD_MINUTES=10
```

### **2. Market-Specific Hold Times**
Set different hold times for each trading pair.
```env
HOLD_TIME_BTC=15     # Hold BTC for 15 minutes
HOLD_TIME_ETH=8      # Hold ETH for 8 minutes  
HOLD_TIME_HYPE=2     # Hold HYPE for 2 minutes (volatile)
HOLD_TIME_SOL=5      # Hold SOL for 5 minutes
HOLD_TIME_BNB=12     # Hold BNB for 12 minutes
```

### **3. Volatility-Based Hold Times**
Automatically adjusts hold times based on asset volatility.
```env
USE_VOLATILITY_BASED_HOLDS=true
```
- **High volatility** (HYPE): Shorter holds (1-3 minutes)
- **Medium volatility** (SOL, BNB): Medium holds (3-7 minutes)  
- **Low volatility** (BTC, ETH): Longer holds (5-10 minutes)

## 🔧 **Configuration Priority**

The bot uses this priority order:
1. **Market-specific** hold times (if set > 0)
2. **Legacy** fixed hold time (if POSITION_HOLD_MINUTES > 0)
3. **Volatility-based** (if enabled)
4. **Random** between MIN/MAX (default)

## 📊 **Example Configurations**

### **Conservative Trading (Longer Holds)**
```env
MIN_POSITION_HOLD_MINUTES=10
MAX_POSITION_HOLD_MINUTES=30

# Market-specific for stability
HOLD_TIME_BTC=20     # Stable, longer holds
HOLD_TIME_ETH=15     # Medium holds
HOLD_TIME_SOL=12     # Shorter for volatility

USE_VOLATILITY_BASED_HOLDS=false
```

### **Aggressive Scalping (Quick Holds)**
```env
MIN_POSITION_HOLD_MINUTES=1
MAX_POSITION_HOLD_MINUTES=5

# Quick scalping times
HOLD_TIME_BTC=3      # Quick BTC scalps
HOLD_TIME_ETH=2      # Very quick ETH
HOLD_TIME_HYPE=1     # Ultra-quick (most volatile)

USE_VOLATILITY_BASED_HOLDS=true
```

### **Mixed Strategy (Random + Market-Specific)**
```env
MIN_POSITION_HOLD_MINUTES=3
MAX_POSITION_HOLD_MINUTES=12

# Only set specific times for some pairs
HOLD_TIME_BTC=15     # Always hold BTC longer
HOLD_TIME_HYPE=2     # Always quick HYPE trades
# ETH, SOL, BNB use random 3-12 minutes

USE_VOLATILITY_BASED_HOLDS=false
```

## 📈 **Enhanced Logging**

The bot now shows detailed hold time information:

```
INFO - Position opened: ETH SHORT - will hold for 7 minutes (random)
INFO - Current position: ETH SHORT (held for 3.2/7 minutes)
INFO - Position opened: BTC LONG - will hold for 15 minutes (market-specific (BTC))
INFO - Position opened: HYPE SHORT - will hold for 2 minutes (volatility-based)
```

## 🎛️ **Migration from Fixed Hold Times**

### **Old Configuration (Deprecated)**
```env
POSITION_HOLD_MINUTES=5  # Fixed 5 minutes for all positions
```

### **New Dynamic Configuration**
```env
# Option 1: Random range
MIN_POSITION_HOLD_MINUTES=3
MAX_POSITION_HOLD_MINUTES=8
POSITION_HOLD_MINUTES=0  # 0 = use dynamic

# Option 2: Market-specific
HOLD_TIME_BTC=10
HOLD_TIME_ETH=6
HOLD_TIME_HYPE=3
HOLD_TIME_SOL=5
HOLD_TIME_BNB=8
```

## 🚀 **Benefits of Dynamic Hold Times**

### **🎯 Better Risk Management**
- Shorter holds for volatile assets reduce risk
- Longer holds for stable assets capture trends
- Random timing prevents predictable patterns

### **📊 Improved Performance**
- Market-specific optimization
- Volatility-aware position management
- Flexible strategy adaptation

### **🔧 Enhanced Control**
- Fine-tune each trading pair individually
- Mix random and fixed strategies
- Easy A/B testing of different approaches

## ⚙️ **Advanced Usage**

### **Time-of-Day Strategies**
```env
# Shorter holds during high-volatility hours
MIN_POSITION_HOLD_MINUTES=2
MAX_POSITION_HOLD_MINUTES=6
USE_VOLATILITY_BASED_HOLDS=true
```

### **Asset-Class Strategies**
```env
# Large caps: longer holds
HOLD_TIME_BTC=15
HOLD_TIME_ETH=12

# Mid caps: medium holds  
HOLD_TIME_SOL=8
HOLD_TIME_BNB=10

# Small caps: quick holds
HOLD_TIME_HYPE=3
```

### **Risk-Adjusted Holds**
```env
# Higher leverage = shorter holds
MIN_POSITION_HOLD_MINUTES=1
MAX_POSITION_HOLD_MINUTES=4
USE_VOLATILITY_BASED_HOLDS=true
```

## 🔍 **Monitoring & Analysis**

Track your hold time performance:
- Monitor which hold times are most profitable
- Adjust based on market conditions
- Use logs to analyze optimal durations per pair

---

**Dynamic hold times give you professional-level position management! 🎯**
