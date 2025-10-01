# Security Policy

## 🔒 Keeping Your Trading Bot Secure

This document outlines security best practices for using the Lighter Trading Bot safely.

## ⚠️ Critical Security Warnings

### 🚨 **NEVER COMMIT SENSITIVE DATA**
- **Never** commit your `.env` file to version control
- **Never** commit `config.py` if it contains API keys
- **Never** share your private keys or API credentials
- **Always** use environment variables for sensitive data

### 🔑 **API Key Security**
- Generate API keys with **minimal required permissions**
- Use **separate API keys** for testing and production
- **Rotate API keys** regularly (monthly recommended)
- **Revoke unused** API keys immediately
- **Monitor API key usage** in your Lighter dashboard

### 💰 **Financial Security**
- **Start with small amounts** - never risk more than you can afford to lose
- **Use separate trading accounts** for bot trading
- **Set strict daily/weekly loss limits**
- **Monitor account balance** regularly
- **Keep most funds in cold storage**, only what you're actively trading in the hot wallet

## 🛡️ Built-in Security Features

### Environment Variable Protection
```bash
# ✅ SECURE - Uses environment variables
LIGHTER_API_KEY_PRIVATE_KEY=your_key_here

# ❌ INSECURE - Hardcoded in source
API_KEY = "your_key_here"  # Never do this!
```

### Process Isolation
- Bot uses file locking to prevent multiple instances
- Graceful shutdown handling prevents data corruption
- Process PID tracking for proper management

### Input Validation
- All configuration values are validated on startup
- Position sizes are capped to prevent over-leveraging
- Trading pairs are restricted to allowed lists

## 🔧 Security Configuration

### Recommended `.env` Security
```bash
# Set restrictive file permissions
chmod 600 .env

# Verify permissions
ls -la .env
# Should show: -rw------- (owner read/write only)
```

### Git Security Setup
```bash
# Ensure .gitignore is properly configured
echo ".env" >> .gitignore
echo "config.py" >> .gitignore
echo "*.log" >> .gitignore

# Check what would be committed
git status
git diff --cached
```

### Network Security
```bash
# If using a proxy, ensure it's secure
USE_PROXY=true
PROXY_URL=https://secure-proxy.example.com:8080

# For development, you can disable SSL verification
# but NEVER do this in production
VERIFY_SSL=true
```

## 🚨 Incident Response

### If Your API Keys Are Compromised
1. **Immediately revoke** the compromised API keys in your Lighter dashboard
2. **Generate new API keys** with minimal permissions
3. **Check your trading history** for unauthorized trades
4. **Update your `.env` file** with new credentials
5. **Review account security** settings

### If You Suspect Unauthorized Trading
1. **Stop the bot immediately**: `python3 start_bot.py stop`
2. **Check recent trades** in your Lighter dashboard
3. **Review bot logs** for suspicious activity
4. **Change API keys** as a precaution
5. **Report to Lighter support** if needed

## 🔍 Security Monitoring

### Regular Security Checks
- **Weekly**: Review trading activity and account balance
- **Monthly**: Rotate API keys and review permissions
- **Quarterly**: Update dependencies and review security settings

### Log Monitoring
```bash
# Check for suspicious activity
grep -i "error\|fail\|unauthorized" trading_bot.log

# Monitor large trades
grep -i "position.*[0-9]{4,}" trading_bot.log
```

### Account Monitoring
- Set up **balance alerts** in your Lighter dashboard
- Monitor **API key usage** statistics
- Review **trading patterns** for anomalies

## 📋 Security Checklist

### Before First Run
- [ ] API keys stored in `.env` file only
- [ ] `.env` file has restrictive permissions (600)
- [ ] `.gitignore` includes all sensitive files
- [ ] Configuration validated with small test amounts
- [ ] Backup of original account balance recorded

### Regular Maintenance
- [ ] API keys rotated monthly
- [ ] Dependencies updated regularly
- [ ] Logs reviewed for anomalies
- [ ] Account balance monitored
- [ ] Trading patterns reviewed

### Before Going Live
- [ ] Tested thoroughly with small amounts
- [ ] All security measures implemented
- [ ] Emergency stop procedures tested
- [ ] Contact information for support ready
- [ ] Risk limits properly configured

## 🆘 Emergency Contacts

### Immediate Actions
- **Stop Bot**: `python3 start_bot.py stop`
- **Kill Process**: `pkill -f random_trading_bot.py`
- **Revoke API Keys**: Visit [Lighter Dashboard](https://app.lighter.xyz/apikeys)

### Support Resources
- **Lighter Support**: [Contact Lighter](https://lighter.xyz/support)
- **GitHub Issues**: [Report Bot Issues](https://github.com/yourusername/lighter-trading-bot/issues)

## 📚 Additional Resources

- [Lighter Security Best Practices](https://docs.lighter.xyz/security)
- [API Key Management Guide](https://docs.lighter.xyz/api-keys)
- [Trading Security Guidelines](https://docs.lighter.xyz/trading-security)

---

**Remember: Security is not a one-time setup, it's an ongoing process. Stay vigilant and trade safely! 🛡️**
