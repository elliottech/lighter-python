#!/usr/bin/env python3
"""
Bot Manager Script - Proper way to start/stop the trading bot
"""

import os
import sys
import subprocess
import signal
import time
import argparse

BOT_SCRIPT = "random_trading_bot.py"
PID_FILE = ".bot.pid"
LOCK_FILE = ".trading_bot.lock"

def get_bot_pid():
    """Get the bot's process ID if running"""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Check if process is actually running
            os.kill(pid, 0)  # This will raise an exception if process doesn't exist
            return pid
        except (OSError, ValueError):
            # Process doesn't exist, remove stale PID file
            os.remove(PID_FILE)
    return None

def start_bot():
    """Start the bot in foreground mode"""
    if get_bot_pid():
        print("❌ Bot is already running!")
        return False
    
    print("🚀 Starting trading bot...")
    
    # Clean up any stale lock files
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
    
    try:
        # Start bot process
        process = subprocess.Popen([sys.executable, BOT_SCRIPT])
        
        # Save PID
        with open(PID_FILE, 'w') as f:
            f.write(str(process.pid))
        
        print(f"✅ Bot started with PID: {process.pid}")
        print("📊 Use 'python3 start_bot.py status' to check status")
        print("🛑 Use 'python3 start_bot.py stop' to stop gracefully")
        print("📋 Use 'python3 start_bot.py logs' to view logs")
        
        # Wait for process to finish
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Received Ctrl+C, stopping bot...")
        stop_bot()
    finally:
        # Clean up PID file
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)

def stop_bot():
    """Stop the bot gracefully"""
    pid = get_bot_pid()
    if not pid:
        print("❌ Bot is not running!")
        return False
    
    print(f"🛑 Stopping bot (PID: {pid})...")
    
    try:
        # Send SIGTERM for graceful shutdown
        os.kill(pid, signal.SIGTERM)
        
        # Wait up to 10 seconds for graceful shutdown
        for i in range(10):
            try:
                os.kill(pid, 0)  # Check if still running
                time.sleep(1)
                print(f"⏳ Waiting for graceful shutdown... ({i+1}/10)")
            except OSError:
                print("✅ Bot stopped gracefully!")
                break
        else:
            # Force kill if still running
            print("⚠️  Forcing bot shutdown...")
            os.kill(pid, signal.SIGKILL)
            print("✅ Bot force stopped!")
        
        # Clean up files
        for file in [PID_FILE, LOCK_FILE]:
            if os.path.exists(file):
                os.remove(file)
                
        return True
        
    except OSError as e:
        print(f"❌ Error stopping bot: {e}")
        return False

def bot_status():
    """Check bot status"""
    pid = get_bot_pid()
    if pid:
        print(f"✅ Bot is running (PID: {pid})")
        
        # Show recent logs
        if os.path.exists("trading_bot.log"):
            print("\n📋 Recent activity:")
            subprocess.run(["tail", "-5", "trading_bot.log"])
    else:
        print("❌ Bot is not running")

def show_logs():
    """Show bot logs"""
    if os.path.exists("trading_bot.log"):
        print("📋 Bot logs (last 20 lines):")
        subprocess.run(["tail", "-20", "trading_bot.log"])
    else:
        print("❌ No log file found")

def main():
    parser = argparse.ArgumentParser(description="Trading Bot Manager")
    parser.add_argument("action", choices=["start", "stop", "status", "logs", "restart"], 
                       help="Action to perform")
    
    args = parser.parse_args()
    
    if args.action == "start":
        start_bot()
    elif args.action == "stop":
        stop_bot()
    elif args.action == "status":
        bot_status()
    elif args.action == "logs":
        show_logs()
    elif args.action == "restart":
        print("🔄 Restarting bot...")
        stop_bot()
        time.sleep(2)
        start_bot()

if __name__ == "__main__":
    main()
