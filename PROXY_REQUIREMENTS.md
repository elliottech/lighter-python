# 🔒 Mandatory Proxy Configuration

## ⚠️ **CRITICAL REQUIREMENT**

**This trading bot REQUIRES a proxy server to function properly. Proxy usage is not optional.**

## 🎯 **Why Proxy is Mandatory**

- **Network Security**: All API requests are routed through secure proxy
- **IP Protection**: Prevents direct IP exposure to trading endpoints
- **Rate Limiting**: Proxy helps manage API request rates
- **Compliance**: Required for proper network isolation

## 🔧 **Proxy Configuration**

### **Required Environment Variables**
```env
# MANDATORY - Always set to true
USE_PROXY=true

# REQUIRED - Your actual proxy credentials
PROXY_URL=http://username:password@proxy.host.com:port
```

### **Proxy URL Format**
```
http://username:password@host:port
https://username:password@host:port
```

**Example:**
```env
PROXY_URL=http://myuser:mypass@proxy.example.com:8080
```

## ✅ **Configuration Validation**

The bot automatically validates your proxy configuration:

### **✅ Valid Configuration**
```env
USE_PROXY=true
PROXY_URL=http://myuser:mypass@192.168.1.100:8080
```

### **❌ Invalid Configurations**

**Missing proxy URL:**
```env
USE_PROXY=true
PROXY_URL=
# Error: PROXY_URL is required when USE_PROXY is true
```

**Example values not updated:**
```env
USE_PROXY=true
PROXY_URL=http://username:password@proxy.example.com:8080
# Error: PROXY_URL is still using example values
```

**Missing authentication:**
```env
USE_PROXY=true
PROXY_URL=http://proxy.example.com:8080
# Error: PROXY_URL must include authentication credentials
```

**Wrong protocol:**
```env
USE_PROXY=true
PROXY_URL=socks5://user:pass@proxy.com:1080
# Error: PROXY_URL must start with http:// or https://
```

## 🚀 **Setup Process**

### **1. Get Your Proxy Credentials**
Obtain proxy server details from your provider:
- Host/IP address
- Port number
- Username
- Password

### **2. Update Configuration**
```bash
# Copy environment template
cp env.example .env

# Edit with your actual proxy credentials
nano .env
```

### **3. Validate Configuration**
```bash
# Run setup script to validate
python3 setup.py

# Should show:
# ✅ Configuration validation passed
# ✅ Proxy configured: http://myuser@***
```

### **4. Start Bot**
```bash
python3 start_bot.py start
```

## 🔍 **Troubleshooting**

### **"Configuration validation failed" Error**
- Check that `PROXY_URL` is not empty
- Ensure you've replaced example values with real credentials
- Verify the URL format includes `http://` or `https://`
- Confirm authentication credentials are included

### **"Connection failed" Error**
- Verify proxy server is accessible
- Check username/password are correct
- Ensure proxy server allows HTTPS traffic
- Test proxy connection independently

### **"SSL Certificate" Errors**
- The bot automatically handles SSL issues with proxies
- If problems persist, check proxy server SSL configuration

## 📋 **Example Configurations**

### **Basic HTTP Proxy**
```env
USE_PROXY=true
PROXY_URL=http://trader123:securepass@proxy.mycompany.com:8080
```

### **HTTPS Proxy**
```env
USE_PROXY=true
PROXY_URL=https://trader123:securepass@secure-proxy.mycompany.com:8443
```

### **IP-based Proxy**
```env
USE_PROXY=true
PROXY_URL=http://trader123:securepass@192.168.1.100:3128
```

## ⚠️ **Security Notes**

- **Never commit** your `.env` file with real proxy credentials
- **Use strong passwords** for proxy authentication
- **Rotate credentials** regularly for security
- **Monitor proxy logs** for unusual activity

## 🆘 **Support**

If you encounter proxy-related issues:

1. **Verify credentials** with your proxy provider
2. **Test connectivity** outside the bot first
3. **Check firewall settings** that might block proxy traffic
4. **Review proxy server logs** for connection attempts

---

**Remember: The bot will NOT start without proper proxy configuration! 🔒**
