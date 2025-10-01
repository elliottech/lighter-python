#!/usr/bin/env python3
"""
Setup script for the Lighter Random Trading Bot

This script helps users set up the trading bot by:
1. Checking dependencies
2. Creating configuration file
3. Validating API connection
4. Running initial tests
"""

import os
import sys
import asyncio
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    
    requirements_files = [
        "requirements.txt",
        "trading_bot_requirements.txt"
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"Installing from {req_file}...")
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", "-r", req_file
                ])
                print(f"✅ Installed dependencies from {req_file}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies from {req_file}: {e}")
                return False
        else:
            print(f"⚠️  {req_file} not found, skipping...")
    
    return True

def create_config_file():
    """Create configuration file from example"""
    config_file = "config.py"
    example_file = "config.example.py"
    
    if os.path.exists(config_file):
        response = input(f"\n⚠️  {config_file} already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Keeping existing configuration file")
            return True
    
    if not os.path.exists(example_file):
        print(f"❌ {example_file} not found")
        return False
    
    try:
        with open(example_file, 'r') as src:
            content = src.read()
        
        with open(config_file, 'w') as dst:
            dst.write(content)
        
        print(f"✅ Created {config_file} from {example_file}")
        print(f"\n📝 Please edit {config_file} with your actual credentials:")
        print("   - API_KEY_PRIVATE_KEY")
        print("   - ACCOUNT_INDEX") 
        print("   - API_KEY_INDEX")
        print("\n   Get your API keys from: https://app.lighter.xyz/apikeys")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create config file: {e}")
        return False

def validate_config():
    """Validate configuration file"""
    try:
        import config
        
        # Check required fields
        required_fields = [
            'API_KEY_PRIVATE_KEY',
            'ACCOUNT_INDEX',
            'API_KEY_INDEX'
        ]
        
        for field in required_fields:
            if not hasattr(config, field):
                print(f"❌ Missing required field: {field}")
                return False
        
        # Check if using example values
        if config.API_KEY_PRIVATE_KEY.startswith("0x1234"):
            print("❌ Please update API_KEY_PRIVATE_KEY with your actual key")
            return False
        
        if config.ACCOUNT_INDEX <= 0:
            print("❌ Please set a valid ACCOUNT_INDEX")
            return False
        
        print("✅ Configuration file looks good")
        return True
        
    except ImportError:
        print("❌ config.py not found or has syntax errors")
        return False
    except Exception as e:
        print(f"❌ Error validating config: {e}")
        return False

async def test_connection():
    """Test connection to Lighter API"""
    print("\n🔗 Testing connection to Lighter API...")
    
    try:
        import lighter
        from config import MAINNET_URL, API_KEY_PRIVATE_KEY, ACCOUNT_INDEX, API_KEY_INDEX
        
        # Test basic API connection
        api_client = lighter.ApiClient(
            configuration=lighter.Configuration(host=MAINNET_URL)
        )
        
        # Test SignerClient
        client = lighter.SignerClient(
            url=MAINNET_URL,
            private_key=API_KEY_PRIVATE_KEY,
            account_index=ACCOUNT_INDEX,
            api_key_index=API_KEY_INDEX,
        )
        
        # Verify client
        err = client.check_client()
        if err:
            print(f"❌ Client verification failed: {err}")
            return False
        
        # Test market data
        order_api = lighter.OrderApi(api_client)
        order_books = await order_api.order_books()
        
        print(f"✅ Successfully connected to Lighter mainnet")
        print(f"✅ Found {len(order_books.order_books)} available markets")
        
        # Cleanup
        await client.close()
        await api_client.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Review your configuration in config.py")
    print("2. Start with small position sizes for testing")
    print("3. Run the bot: python random_trading_bot.py")
    print("4. Monitor the logs: tail -f trading_bot.log")
    print("\n⚠️  Important reminders:")
    print("- This is for educational purposes only")
    print("- Start with small amounts to test")
    print("- Monitor your positions actively")
    print("- Never risk more than you can afford to lose")

async def main():
    """Main setup process"""
    print("🚀 Lighter Random Trading Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create config file
    if not create_config_file():
        return 1
    
    # Wait for user to update config
    input("\n⏸️  Press Enter after updating config.py with your credentials...")
    
    # Validate config
    if not validate_config():
        print("\n❌ Please fix the configuration issues and run setup again")
        return 1
    
    # Test connection
    if not await test_connection():
        print("\n❌ Connection test failed. Please check your credentials")
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
