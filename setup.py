#!/usr/bin/env python3
"""
Setup script for Lighter Trading Bot
"""

import os
import sys
import subprocess
import shutil

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "trading_bot_requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_environment():
    """Set up environment configuration"""
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            shutil.copy("env.example", ".env")
            print("✅ Created .env file from template")
            print("⚠️  IMPORTANT: Edit .env file with your actual Lighter API credentials!")
        else:
            print("❌ env.example not found")
            return False
    else:
        print("✅ .env file already exists")
    return True

def check_git_setup():
    """Check if git is properly configured"""
    if os.path.exists(".git"):
        print("✅ Git repository detected")
        
        # Check if sensitive files are in gitignore
        if os.path.exists(".gitignore"):
            with open(".gitignore", "r") as f:
                gitignore_content = f.read()
            
            sensitive_files = [".env", "config.py", "*.log"]
            missing_files = []
            
            for file_pattern in sensitive_files:
                if file_pattern not in gitignore_content:
                    missing_files.append(file_pattern)
            
            if missing_files:
                print(f"⚠️  Warning: These sensitive files are not in .gitignore: {missing_files}")
            else:
                print("✅ Sensitive files are properly ignored")
        else:
            print("⚠️  No .gitignore found - sensitive data might be committed!")
    else:
        print("ℹ️  Not a git repository")

def validate_config():
    """Validate configuration"""
    try:
        # Try to import config to check for errors
        import config
        print("✅ Configuration validation passed")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        print("💡 Make sure to edit your .env file with correct values")
        return False

def main():
    """Main setup function"""
    print("🚀 Lighter Trading Bot Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Check git setup
    check_git_setup()
    
    # Validate configuration
    config_valid = validate_config()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed!")
    
    if config_valid:
        print("\n✅ Your bot is ready to run:")
        print("   python3 start_bot.py start")
    else:
        print("\n⚠️  Next steps:")
        print("   1. Edit .env file with your Lighter API credentials")
        print("   2. Run: python3 start_bot.py start")
    
    print("\n📚 Documentation:")
    print("   - README.md for usage instructions")
    print("   - env.example for configuration options")
    
    print("\n⚠️  Remember:")
    print("   - This is experimental software")
    print("   - Never trade more than you can afford to lose")
    print("   - Test with small amounts first")

if __name__ == "__main__":
    main()