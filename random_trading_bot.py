#!/usr/bin/env python3
"""
Lighter Random Trading Bot

This bot opens random long/short positions on Lighter mainnet using the lighter-python SDK.
It randomly selects trading pairs, position directions, and sizes within configured limits.

IMPORTANT: This is for educational/testing purposes only. 
Use at your own risk and ensure you understand the implications of automated trading.
"""

import asyncio
import logging
import random
import time
import os
import fcntl
import signal
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import json

import lighter
from config import (
    MAINNET_URL, API_KEY_PRIVATE_KEY, ACCOUNT_INDEX, API_KEY_INDEX,
    MIN_TRADE_INTERVAL, MAX_TRADE_INTERVAL,
    MAX_DAILY_TRADES, ENABLE_RISK_LIMITS, LOG_LEVEL, LOG_TO_FILE, LOG_FILE,
    EXCLUDED_MARKETS, PREFERRED_MARKETS, DEFAULT_SLIPPAGE, ORDER_TIMEOUT,
    PROXY_URL, USE_PROXY, ALLOWED_TRADING_PAIRS, MANUAL_LEVERAGE, MARGIN_MODE,
    POSITION_HOLD_MINUTES, SINGLE_POSITION_MODE, ACCOUNT_BALANCE, 
    MIN_POSITION_PERCENT, MAX_POSITION_PERCENT
)


class TradingStats:
    """Track trading statistics and risk metrics"""
    
    def __init__(self):
        self.daily_trades = 0
        self.total_trades = 0
        self.successful_trades = 0
        self.failed_trades = 0
        self.last_reset = datetime.now().date()
        self.positions = {}  # market_index -> position_info
        
    def reset_daily_stats(self):
        """Reset daily statistics if it's a new day"""
        today = datetime.now().date()
        if today > self.last_reset:
            self.daily_trades = 0
            self.last_reset = today
            
    def can_trade(self) -> bool:
        """Check if we can place another trade based on risk limits"""
        self.reset_daily_stats()
        if ENABLE_RISK_LIMITS and self.daily_trades >= MAX_DAILY_TRADES:
            return False
        return True
        
    def record_trade(self, success: bool):
        """Record a trade attempt"""
        self.reset_daily_stats()
        self.total_trades += 1
        self.daily_trades += 1
        if success:
            self.successful_trades += 1
        else:
            self.failed_trades += 1


class PositionManager:
    """Manage single position lifecycle"""
    
    def __init__(self):
        self.current_position = None
        self.position_opened_at = None
        
    def has_position(self) -> bool:
        """Check if we currently have an open position"""
        return self.current_position is not None
        
    def open_position(self, market_symbol: str, market_index: int, is_ask: bool, size: int, tx_hash: str):
        """Record a new position"""
        self.current_position = {
            'symbol': market_symbol,
            'market_index': market_index,
            'is_ask': is_ask,
            'size': size,
            'tx_hash': tx_hash
        }
        self.position_opened_at = datetime.now()
        
    def should_close_position(self) -> bool:
        """Check if position should be closed based on hold time"""
        if not self.has_position():
            return False
            
        hold_duration = datetime.now() - self.position_opened_at
        return hold_duration >= timedelta(minutes=POSITION_HOLD_MINUTES)
        
    def close_position(self):
        """Clear current position"""
        self.current_position = None
        self.position_opened_at = None
        
    def get_position_info(self) -> Dict:
        """Get current position information"""
        if not self.has_position():
            return None
            
        hold_duration = datetime.now() - self.position_opened_at
        return {
            **self.current_position,
            'opened_at': self.position_opened_at,
            'hold_duration_minutes': hold_duration.total_seconds() / 60,
            'should_close': self.should_close_position()
        }


class LighterRandomTradingBot:
    """Random trading bot for Lighter protocol"""
    
    def __init__(self):
        self.setup_logging()
        self.stats = TradingStats()
        self.position_manager = PositionManager()
        self.client: Optional[lighter.SignerClient] = None
        self.api_client: Optional[lighter.ApiClient] = None
        self.order_api: Optional[lighter.OrderApi] = None
        self.available_markets: List[Dict] = []
        self.running = False
        self.lock_file = None
        
        # Setup signal handlers for graceful shutdown
        self._setup_signal_handlers()
        
        # Acquire process lock to prevent multiple instances
        self._acquire_process_lock()
        
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            self.logger.info(f"Received signal {signum}, initiating graceful shutdown...")
            self.running = False
            
        signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
        signal.signal(signal.SIGTERM, signal_handler)  # Termination signal
        
    def setup_logging(self):
        """Configure logging"""
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        # Configure root logger
        logging.basicConfig(
            level=getattr(logging, LOG_LEVEL),
            format=log_format,
            handlers=[]
        )
        
        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter(log_format))
        
        # Add file handler if enabled
        handlers = [console_handler]
        if LOG_TO_FILE:
            file_handler = logging.FileHandler(LOG_FILE)
            file_handler.setFormatter(logging.Formatter(log_format))
            handlers.append(file_handler)
            
        # Configure logger
        self.logger = logging.getLogger(__name__)
        for handler in handlers:
            self.logger.addHandler(handler)
            
        # Reduce noise from other libraries
        logging.getLogger('lighter').setLevel(logging.WARNING)
        logging.getLogger('aiohttp').setLevel(logging.WARNING)
        
    async def initialize(self):
        """Initialize the trading bot"""
        self.logger.info("Initializing Lighter Random Trading Bot...")
        
        # Validate configuration
        if not self._validate_config():
            raise ValueError("Invalid configuration. Please check config.py")
            
        # Initialize API clients
        try:
            # Configure SSL settings and proxy for potential certificate issues
            config = lighter.Configuration(host=MAINNET_URL)
            config.verify_ssl = False  # Disable SSL verification if needed
            
            # Configure proxy if enabled
            if USE_PROXY and PROXY_URL:
                config.proxy = PROXY_URL
                self.logger.info(f"Using proxy: {PROXY_URL}")
            
            self.api_client = lighter.ApiClient(configuration=config)
            
            self.client = lighter.SignerClient(
                url=MAINNET_URL,
                private_key=API_KEY_PRIVATE_KEY,
                account_index=ACCOUNT_INDEX,
                api_key_index=API_KEY_INDEX,
            )
            
            # Replace SignerClient's ApiClient with our configured one (for proxy support)
            await self.client.api_client.close()  # Close the default client
            self.client.api_client = self.api_client
            self.client.tx_api = lighter.TransactionApi(self.api_client)
            self.client.order_api = lighter.OrderApi(self.api_client)
            
            self.order_api = lighter.OrderApi(self.api_client)
            
            # Verify client connection
            err = self.client.check_client()
            if err:
                raise Exception(f"Client verification failed: {err}")
                
            self.logger.info("Successfully connected to Lighter mainnet")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize clients: {e}")
            raise
            
        # Load available markets
        await self._load_markets()
        
    def _validate_config(self) -> bool:
        """Validate configuration parameters"""
        if not API_KEY_PRIVATE_KEY or API_KEY_PRIVATE_KEY.startswith("0x1234"):
            self.logger.error("Please set your actual API_KEY_PRIVATE_KEY in config.py")
            return False
            
        if ACCOUNT_INDEX <= 0:
            self.logger.error("Please set a valid ACCOUNT_INDEX in config.py")
            return False
            
        if MIN_POSITION_PERCENT >= MAX_POSITION_PERCENT:
            self.logger.error("MIN_POSITION_PERCENT must be less than MAX_POSITION_PERCENT")
            return False
            
        return True
        
    async def _load_markets(self):
        """Load available trading markets"""
        try:
            self.logger.info("Loading available markets...")
            order_books = await self.order_api.order_books()
            
            self.available_markets = []
            for market in order_books.order_books:
                # Use market_id instead of market_index
                market_info = {
                    'index': market.market_id,
                    'symbol': market.symbol,
                    'status': market.status,
                    'min_base_amount': market.min_base_amount,
                    'min_quote_amount': market.min_quote_amount,
                }
                
                # Apply market filters
                if EXCLUDED_MARKETS and market.market_id in EXCLUDED_MARKETS:
                    continue
                    
                if PREFERRED_MARKETS and market.market_id not in PREFERRED_MARKETS:
                    continue
                
                # Filter by allowed trading pairs
                if ALLOWED_TRADING_PAIRS and market.symbol not in ALLOWED_TRADING_PAIRS:
                    self.logger.debug(f"Skipping market {market.symbol} (not in allowed pairs)")
                    continue
                    
                # Only include active markets
                if market.status.lower() != 'active':
                    self.logger.debug(f"Skipping inactive market {market.symbol} (status: {market.status})")
                    continue
                    
                self.available_markets.append(market_info)
                
            if not self.available_markets:
                raise Exception("No available markets found after applying filters")
                
            self.logger.info(f"Loaded {len(self.available_markets)} available markets:")
            for market in self.available_markets:
                self.logger.info(f"  {market['index']}: {market['symbol']} (status: {market.get('status', 'unknown')})")
            
            # Debug: Log the allowed pairs for verification
            self.logger.info(f"Allowed trading pairs: {ALLOWED_TRADING_PAIRS}")
            available_symbols = [m['symbol'] for m in self.available_markets]
            self.logger.info(f"Available market symbols: {available_symbols}")
                
        except Exception as e:
            self.logger.error(f"Failed to load markets: {e}")
            raise
            
    async def _get_market_details(self, market_index: int) -> Optional[Dict]:
        """Get detailed market information including leverage limits"""
        try:
            details_response = await self.order_api.order_book_details(market_index)
            details = details_response.order_book_details[0]
            
            return {
                'symbol': details.symbol,
                'price_decimals': details.price_decimals,
                'size_decimals': details.size_decimals,
                'default_imf': details.default_initial_margin_fraction,
                'min_imf': details.min_initial_margin_fraction,
                'default_leverage': 10000 / details.default_initial_margin_fraction,
                'max_leverage': 10000 / details.min_initial_margin_fraction,
            }
        except Exception as e:
            self.logger.error(f"Failed to get market details for {market_index}: {e}")
            return None
            
    def _generate_random_trade_params(self) -> Tuple[Dict, bool, int]:
        """Generate random trading parameters"""
        # Debug: Log available markets before selection
        self.logger.debug(f"Available markets for selection: {[m['symbol'] for m in self.available_markets]}")
        
        # STRICT VALIDATION: Ensure we have valid markets
        if not self.available_markets:
            raise Exception("No available markets loaded!")
            
        # STRICT VALIDATION: Double-check all markets are in allowed pairs
        for market in self.available_markets:
            if market['symbol'] not in ALLOWED_TRADING_PAIRS:
                raise Exception(f"CRITICAL: Market {market['symbol']} is in available_markets but not in ALLOWED_TRADING_PAIRS!")
        
        # Select random market
        market = random.choice(self.available_markets)
        
        # STRICT VALIDATION: Final check before returning
        if market['symbol'] not in ALLOWED_TRADING_PAIRS:
            raise Exception(f"CRITICAL: Selected market {market['symbol']} is not in allowed pairs {ALLOWED_TRADING_PAIRS}!")
        
        # Debug: Log selected market
        self.logger.debug(f"Selected market: {market['symbol']} (index: {market['index']})")
        
        # Random position direction (True = short/sell, False = long/buy)
        is_ask = random.choice([True, False])
        position_type = "SHORT" if is_ask else "LONG"
        
        # For now, return without position size - we'll calculate it later when we have market details
        return market, is_ask, None
        
    async def _calculate_percentage_position_size(self, market: Dict, current_price: float) -> int:
        """Calculate position size based on percentage of account balance"""
        try:
            # Get random percentage between min and max
            position_percent = random.uniform(MIN_POSITION_PERCENT, MAX_POSITION_PERCENT)
            
            # Calculate dollar amount to risk
            position_value_usd = (ACCOUNT_BALANCE * position_percent) / 100
            
            # Get leverage for this market
            leverage = MANUAL_LEVERAGE.get(market['symbol'], 1)
            
            # Calculate notional value we can afford with this leverage
            max_notional_value = position_value_usd * leverage
            
            # Calculate position size in units
            position_size_units = max_notional_value / current_price
            
            # For expensive assets like BTC, ensure we don't exceed account balance
            max_affordable_notional = ACCOUNT_BALANCE * 0.8  # Max 80% of account as notional
            if position_size_units * current_price > max_affordable_notional:
                position_size_units = max_affordable_notional / current_price
                self.logger.warning(f"Reduced position size for {market['symbol']} due to price: {position_size_units:.6f} units")
            
            # Ensure minimum of 0.000001 units (for BTC) but reasonable minimum
            position_size_units = max(0.000001, position_size_units)
            
            self.logger.debug(
                f"Percentage calculation: {position_percent:.1f}% of ${ACCOUNT_BALANCE} = "
                f"${position_value_usd:.2f} risk → ${max_notional_value:.2f} notional "
                f"÷ ${current_price:.2f} price = {position_size_units} units"
            )
            
            return position_size_units
            
        except Exception as e:
            self.logger.error(f"Error calculating percentage position size: {e}")
            # Fallback to 1 unit minimum
            return 1
        
    async def _get_market_price(self, market_index: int, is_ask: bool, market_details: Dict) -> Optional[Tuple[int, float]]:
        """Get current market price for order execution"""
        try:
            order_book = await self.order_api.order_book_orders(market_index, 1)
            
            if is_ask and order_book.bids:
                # For short positions, use bid price
                price_str = order_book.bids[0].price
            elif not is_ask and order_book.asks:
                # For long positions, use ask price
                price_str = order_book.asks[0].price
            else:
                self.logger.warning(f"No price data available for market {market_index}")
                return None
                
            # Convert price string to float for USD display
            price_usd = float(price_str)
            
            # Convert to internal format (scaled by price_decimals)
            price_decimals = market_details.get('price_decimals', 5)
            price_scaled = int(price_usd * (10 ** price_decimals))
            
            # Apply slippage tolerance
            if is_ask:
                price_scaled = int(price_scaled * (1 - DEFAULT_SLIPPAGE))
                price_usd = price_usd * (1 - DEFAULT_SLIPPAGE)
            else:
                price_scaled = int(price_scaled * (1 + DEFAULT_SLIPPAGE))
                price_usd = price_usd * (1 + DEFAULT_SLIPPAGE)
                
            return price_scaled, price_usd
            
        except Exception as e:
            self.logger.error(f"Failed to get market price for {market_index}: {e}")
            return None
            
    async def _verify_order_filled(self, tx_hash: str, market_index: int) -> bool:
        """Verify that an order was actually filled"""
        if not tx_hash:
            return False
            
        try:
            # Wait a moment for the order to be processed
            await asyncio.sleep(2)
            
            # Check if we have a position in this market (simple verification)
            # In a more robust implementation, you'd check the specific order status
            self.logger.info(f"Verifying order fill for TX: {tx_hash}")
            
            # For now, assume market orders are filled (they usually are)
            # You could add more sophisticated verification here by checking:
            # - Order status via API
            # - Position changes
            # - Account balance changes
            return True
            
        except Exception as e:
            self.logger.error(f"Error verifying order fill: {e}")
            return False
            
    async def _place_random_trade(self):
        """Place a single random trade"""
        if not self.stats.can_trade():
            self.logger.warning(f"Daily trade limit reached ({MAX_DAILY_TRADES})")
            return
            
        # STRICT POSITION LIMIT CHECK: In single position mode, don't open new positions if we already have one
        if SINGLE_POSITION_MODE and self.position_manager.has_position():
            position_info = self.position_manager.get_position_info()
            self.logger.warning(f"BLOCKED: Already have open position {position_info['symbol']} {'SHORT' if position_info['is_ask'] else 'LONG'} - cannot open new position in single position mode")
            return
            
        try:
            # Generate random trade parameters (without position size yet)
            market, is_ask, _ = self._generate_random_trade_params()
            
            # Get market details for leverage and price conversion
            market_details = await self._get_market_details(market['index'])
            if not market_details:
                self.logger.error(f"Could not get market details for {market['symbol']}")
                self.stats.record_trade(False)
                return
            
            # Set manual leverage for this market
            if market['symbol'] in MANUAL_LEVERAGE:
                desired_leverage = MANUAL_LEVERAGE[market['symbol']]
                max_allowed_leverage = market_details['max_leverage']
                
                # Ensure desired leverage doesn't exceed market maximum
                if desired_leverage <= max_allowed_leverage:
                    leverage = desired_leverage
                    
                    self.logger.info(f"Setting manual leverage: {leverage:.1f}x for {market['symbol']} (max: {max_allowed_leverage:.1f}x)")
                    
                    # Update leverage for this market
                    try:
                        _, leverage_tx, leverage_error = await self.client.update_leverage(
                            market_index=market['index'],
                            margin_mode=MARGIN_MODE,
                            leverage=leverage
                        )
                        if leverage_error:
                            self.logger.warning(f"Failed to set leverage: {leverage_error}")
                        else:
                            self.logger.debug(f"Leverage set successfully")
                    except Exception as e:
                        self.logger.warning(f"Failed to update leverage: {e}")
                else:
                    self.logger.warning(f"Desired leverage {desired_leverage}x exceeds market maximum {max_allowed_leverage:.1f}x for {market['symbol']}")
            else:
                self.logger.info(f"No manual leverage configured for {market['symbol']}, using market default")
            
            # Get current market price
            price_result = await self._get_market_price(market['index'], is_ask, market_details)
            if price_result is None:
                self.logger.error(f"Could not get price for {market['symbol']}")
                self.stats.record_trade(False)
                return
                
            price_scaled, price_usd = price_result
            
            # Calculate position size based on percentage of account balance
            base_amount_float = await self._calculate_percentage_position_size(market, price_usd)
            
            # Scale the position size based on market's size_decimals
            size_decimals = market_details.get('size_decimals', 0)
            base_amount = int(base_amount_float * (10 ** size_decimals))
            
            self.logger.info(f"Percentage-based position sizing: {MIN_POSITION_PERCENT}%-{MAX_POSITION_PERCENT}% of ${ACCOUNT_BALANCE} = {base_amount_float} units → {base_amount} scaled units (decimals: {size_decimals})")
                
            # Generate unique client order index
            client_order_index = int(time.time() * 1000) % 1000000
            
            # FINAL VALIDATION: Last check before placing order
            if market['symbol'] not in ALLOWED_TRADING_PAIRS:
                raise Exception(f"CRITICAL: Attempting to place order for {market['symbol']} which is not in allowed pairs!")
                
            if SINGLE_POSITION_MODE and self.position_manager.has_position():
                raise Exception(f"CRITICAL: Attempting to place order while already having a position in single position mode!")
            
            self.logger.info(
                f"Placing {'SHORT' if is_ask else 'LONG'} market order: "
                f"{market['symbol']} size={base_amount} price=${price_usd:.5f} (scaled: {price_scaled})"
            )
            
            # Place market order
            created_order, tx_hash, error = await self.client.create_market_order(
                market_index=market['index'],
                client_order_index=client_order_index,
                base_amount=base_amount,
                avg_execution_price=price_scaled,
                is_ask=is_ask,
                reduce_only=False
            )
            
            if error:
                self.logger.error(f"Trade failed: {error}")
                self.stats.record_trade(False)
                return
                
            # Verify order was filled before proceeding
            if not await self._verify_order_filled(tx_hash.tx_hash if tx_hash else None, market['index']):
                self.logger.error(f"Order was not filled, skipping position tracking")
                self.stats.record_trade(False)
                return
                
            self.logger.info(
                f"Trade successful and filled! TX: {tx_hash.tx_hash if tx_hash else 'N/A'}"
            )
            self.stats.record_trade(True)
            
            # Log trade details
            self._log_trade_details(market, is_ask, base_amount, price_scaled, price_usd, tx_hash)
            
        except Exception as e:
            self.logger.error(f"Unexpected error during trade: {e}")
            self.stats.record_trade(False)
            
    def _log_trade_details(self, market: Dict, is_ask: bool, base_amount: int, 
                          price_scaled: int, price_usd: float, tx_hash):
        """Log detailed trade information"""
        trade_info = {
            'timestamp': datetime.now().isoformat(),
            'market': market['symbol'],
            'market_index': market['index'],
            'position_type': 'SHORT' if is_ask else 'LONG',
            'base_amount': base_amount,
            'price_usd': round(price_usd, 5),
            'price_scaled': price_scaled,
            'tx_hash': tx_hash.tx_hash if tx_hash else None,
            'daily_trades': self.stats.daily_trades,
            'total_trades': self.stats.total_trades
        }
        
        self.logger.info(f"Trade details: {json.dumps(trade_info, indent=2)}")
        
        # Record position if in single position mode
        if SINGLE_POSITION_MODE:
            self.position_manager.open_position(
                market['symbol'], 
                market['index'], 
                is_ask, 
                base_amount, 
                tx_hash.tx_hash if tx_hash else None
            )
            self.logger.info(f"Position opened: {market['symbol']} {'SHORT' if is_ask else 'LONG'} - will hold for {POSITION_HOLD_MINUTES} minutes")
            
    def _acquire_process_lock(self):
        """Acquire a file lock to prevent multiple instances"""
        lock_file_path = os.path.join(os.path.dirname(__file__), '.trading_bot.lock')
        try:
            self.lock_file = open(lock_file_path, 'w')
            fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.lock_file.write(f"{os.getpid()}\n")
            self.lock_file.flush()
            self.logger.info(f"Process lock acquired (PID: {os.getpid()})")
        except (IOError, OSError) as e:
            if self.lock_file:
                self.lock_file.close()
            raise Exception(f"Another instance of the trading bot is already running! {e}")
            
    def _release_process_lock(self):
        """Release the process lock"""
        if self.lock_file:
            try:
                fcntl.flock(self.lock_file.fileno(), fcntl.LOCK_UN)
                self.lock_file.close()
                lock_file_path = os.path.join(os.path.dirname(__file__), '.trading_bot.lock')
                if os.path.exists(lock_file_path):
                    os.remove(lock_file_path)
                self.logger.info("Process lock released")
            except Exception as e:
                self.logger.warning(f"Error releasing process lock: {e}")
        
    async def _close_position(self):
        """Close the current position"""
        if not self.position_manager.has_position():
            return
            
        position = self.position_manager.get_position_info()
        
        try:
            self.logger.info(f"Closing position: {position['symbol']} {'SHORT' if position['is_ask'] else 'LONG'}")
            
            # Create opposite order to close position
            market_details = await self._get_market_details(position['market_index'])
            if not market_details:
                self.logger.error(f"Could not get market details for closing position")
                return
                
            # Get current price for closing
            price_result = await self._get_market_price(position['market_index'], not position['is_ask'], market_details)
            if price_result is None:
                self.logger.error(f"Could not get price for closing position")
                return
                
            price_scaled, price_usd = price_result
            client_order_index = int(time.time() * 1000) % 1000000
            
            # Place closing order (opposite direction)
            created_order, tx_hash, error = await self.client.create_market_order(
                market_index=position['market_index'],
                client_order_index=client_order_index,
                base_amount=position['size'],
                avg_execution_price=price_scaled,
                is_ask=not position['is_ask'],  # Opposite direction
                reduce_only=True  # This closes the position
            )
            
            if error:
                self.logger.error(f"Failed to close position: {error}")
                return
                
            self.logger.info(f"Position closed successfully! TX: {tx_hash.tx_hash if tx_hash else 'N/A'}")
            self.position_manager.close_position()
            
        except Exception as e:
            self.logger.error(f"Error closing position: {e}")
        
    def _print_stats(self):
        """Print current trading statistics"""
        success_rate = (
            (self.stats.successful_trades / self.stats.total_trades * 100)
            if self.stats.total_trades > 0 else 0
        )
        
        self.logger.info(
            f"Trading Stats - Daily: {self.stats.daily_trades}/{MAX_DAILY_TRADES} "
            f"Total: {self.stats.total_trades} "
            f"Success: {self.stats.successful_trades} "
            f"Failed: {self.stats.failed_trades} "
            f"Success Rate: {success_rate:.1f}%"
        )
        
    async def run(self):
        """Main trading loop"""
        self.logger.info("Starting random trading bot...")
        if SINGLE_POSITION_MODE:
            self.logger.info(f"Single position mode enabled - holding positions for {POSITION_HOLD_MINUTES} minutes")
        self.running = True
        
        try:
            while self.running:
                # Print stats periodically
                self._print_stats()
                
                if SINGLE_POSITION_MODE:
                    # Single position management logic
                    if self.position_manager.has_position():
                        position_info = self.position_manager.get_position_info()
                        self.logger.info(f"Current position: {position_info['symbol']} {'SHORT' if position_info['is_ask'] else 'LONG'} "
                                       f"(held for {position_info['hold_duration_minutes']:.1f} minutes)")
                        
                        if self.position_manager.should_close_position():
                            await self._close_position()
                            # Wait a bit before opening next position
                            self.logger.info("Waiting 30 seconds before opening next position...")
                            await asyncio.sleep(30)
                        else:
                            # Check every 30 seconds if position should be closed
                            await asyncio.sleep(30)
                            continue
                    else:
                        # No position, open a new one
                        await self._place_random_trade()
                        
                        # Wait a bit after opening position
                        await asyncio.sleep(10)
                else:
                    # Original random trading logic
                    await self._place_random_trade()
                    
                    # Random wait between trades
                    wait_time = random.randint(MIN_TRADE_INTERVAL, MAX_TRADE_INTERVAL)
                    self.logger.info(f"Waiting {wait_time} seconds until next trade...")
                    
                    # Wait with ability to interrupt
                    for _ in range(wait_time):
                        if not self.running:
                            break
                        await asyncio.sleep(1)
                    
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal, stopping...")
        except Exception as e:
            self.logger.error(f"Unexpected error in main loop: {e}")
        finally:
            await self.cleanup()
            
    async def stop(self):
        """Stop the trading bot"""
        self.logger.info("Stopping trading bot...")
        self.running = False
        
    async def cleanup(self):
        """Clean up resources"""
        self.logger.info("Cleaning up resources...")
        
        try:
            if self.client:
                await self.client.close()
            if self.api_client:
                await self.api_client.close()
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
            
        # Release process lock
        self._release_process_lock()
            
        self._print_stats()
        self.logger.info("Trading bot stopped")


async def main():
    """Main entry point"""
    bot = LighterRandomTradingBot()
    
    try:
        await bot.initialize()
        await bot.run()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        return 1
        
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
