#!/usr/bin/env python3
"""
PnL Fee Comparison Tool

This script generates a dual-plot visualization comparing time-series PnL 
for a given L1 address with 0% fees (current) vs 0.05% taker fees.
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Union
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), 'lighter'))

from lighter.models.trade import Trade
from lighter.models.account import Account

class PnLFeeComparison:
    def __init__(self):
        self.taker_fee_rate = 0.0005  # 0.05%
    
    def identify_taker_account(self, trade: Trade, target_l1_address: str) -> bool:
        """
        Determine if the target L1 address is the taker in this trade.
        
        Logic: 
        - If is_maker_ask is True, the ask side is the maker, so bid side is taker
        - If is_maker_ask is False, the bid side is the maker, so ask side is taker
        """
        ask_l1 = trade.additional_properties.get('ask_account_l1')
        bid_l1 = trade.additional_properties.get('bid_account_l1')
        
        if not ask_l1 or not bid_l1:
            return False
            
        if trade.is_maker_ask:
            return bid_l1 == target_l1_address
        else:
            return ask_l1 == target_l1_address
    
    def calculate_taker_fee(self, trade: Trade, target_l1_address: str) -> float:
        """Calculate the taker fee for this trade if the target address is the taker."""
        if self.identify_taker_account(trade, target_l1_address):
            return float(trade.usd_amount) * self.taker_fee_rate
        return 0.0
    
    def identify_taker_account_simple(self, ask_l1: str, bid_l1: str, is_maker_ask: bool, target_l1: str) -> bool:
        """Helper method to identify taker for sample data generation."""
        if is_maker_ask:
            return bid_l1 == target_l1
        else:
            return ask_l1 == target_l1
    
    def get_sample_trades(self, l1_address: str, days_back: int = 30) -> List[Trade]:
        """Generate sample trade data for testing purposes."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days_back)
        
        trades = []
        current_time = start_time
        
        for i in range(50):
            current_time += timedelta(hours=2, minutes=np.random.randint(0, 120))
            if current_time > end_time:
                break
            
            is_maker_ask = bool(np.random.choice([True, False]))
            price = 50000 + np.random.normal(0, 5000)
            size = np.random.uniform(0.01, 1.0)
            cost = price * size
            
            if np.random.choice([True, False]):
                ask_l1 = l1_address
                bid_l1 = f"0x{''.join(np.random.choice(list('0123456789abcdef'), 40))}"
            else:
                bid_l1 = l1_address
                ask_l1 = f"0x{''.join(np.random.choice(list('0123456789abcdef'), 40))}"
            
            timestamp_ms = int(current_time.timestamp() * 1000)
            
            trade_dict = {
                'trade_id': i,
                'tx_hash': f"0x{''.join(np.random.choice(list('0123456789abcdef'), 64))}",
                'type': "trade",
                'market_id': 1,
                'size': f"{size:.8f}",
                'price': f"{price:.2f}",
                'usd_amount': f"{cost:.6f}",
                'ask_id': 1000 + i,
                'bid_id': 2000 + i,
                'ask_account_id': 1000 + i,
                'bid_account_id': 2000 + i,
                'is_maker_ask': is_maker_ask,
                'block_height': 1000000 + i,
                'timestamp': timestamp_ms,
                'taker_fee': int(cost * 0.0005 * 1000000) if self.identify_taker_account_simple(ask_l1, bid_l1, is_maker_ask, l1_address) else None,
                'taker_position_size_before': "0.0",
                'taker_entry_quote_before': "0.0",
                'taker_initial_margin_fraction_before': 100000,
                'taker_position_sign_changed': False,
                'maker_fee': 0,
                'maker_position_size_before': "0.0",
                'maker_entry_quote_before': "0.0",
                'maker_initial_margin_fraction_before': 100000,
                'maker_position_sign_changed': False,
                'ask_account_l1': ask_l1,
                'bid_account_l1': bid_l1
            }
            
            trade = Trade.from_dict(trade_dict)
            trades.append(trade)
        
        return sorted(trades, key=lambda t: t.timestamp)
    
    def get_pnl_with_fees(self, l1_address: str, trades: List[Trade]) -> Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]:
        """
        Calculate time-series PnL data with and without taker fees.
        
        Returns:
            Tuple of (pnl_no_fees, pnl_with_fees) where each is a list of (timestamp, cumulative_pnl) tuples
        """
        if not trades:
            return [], []
        
        pnl_no_fees = []
        pnl_with_fees = []
        
        cumulative_pnl_no_fees = 0.0
        cumulative_pnl_with_fees = 0.0
        position = 0.0
        avg_entry_price = 0.0
        
        for trade in trades:
            timestamp = float(trade.timestamp) / 1000.0
            
            ask_l1 = trade.additional_properties.get('ask_account_l1')
            bid_l1 = trade.additional_properties.get('bid_account_l1')
            
            if not ask_l1 or not bid_l1:
                continue
            
            if ask_l1 == l1_address:
                trade_pnl = float(trade.size) * (float(trade.price) - avg_entry_price) if position > 0 else 0
                position -= float(trade.size)
            elif bid_l1 == l1_address:
                if position <= 0:
                    avg_entry_price = float(trade.price)
                else:
                    avg_entry_price = (avg_entry_price * position + float(trade.price) * float(trade.size)) / (position + float(trade.size))
                position += float(trade.size)
                trade_pnl = 0
            else:
                continue
            
            taker_fee = self.calculate_taker_fee(trade, l1_address)
            
            cumulative_pnl_no_fees += trade_pnl
            cumulative_pnl_with_fees += trade_pnl - taker_fee
            
            pnl_no_fees.append((timestamp, cumulative_pnl_no_fees))
            pnl_with_fees.append((timestamp, cumulative_pnl_with_fees))
        
        return pnl_no_fees, pnl_with_fees
    
    def create_dual_plot(self, l1_address: str, pnl_no_fees: List[Tuple[float, float]], 
                        pnl_with_fees: List[Tuple[float, float]], output_file: str = None):
        """Create a dual-plot visualization of PnL with and without fees."""
        if not pnl_no_fees or not pnl_with_fees:
            print("No data to plot")
            return
        
        df_no_fees = pd.DataFrame(pnl_no_fees, columns=['timestamp', 'pnl'])
        df_with_fees = pd.DataFrame(pnl_with_fees, columns=['timestamp', 'pnl'])
        
        df_no_fees['datetime'] = pd.to_datetime(df_no_fees['timestamp'], unit='s')
        df_with_fees['datetime'] = pd.to_datetime(df_with_fees['timestamp'], unit='s')
        
        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.patch.set_facecolor('#1a1a1a')
        ax.set_facecolor('#1a1a1a')
        
        ax.plot(df_no_fees['datetime'], df_no_fees['pnl'], 
                label='PnL (0% fees)', linewidth=2, color='#00ff88')
        ax.plot(df_with_fees['datetime'], df_with_fees['pnl'], 
                label='PnL (0.05% taker fees)', linewidth=2, color='#ff6b6b')
        
        ax.set_title(f'Cumulative PnL Comparison for {l1_address[:10]}...', 
                    fontsize=16, fontweight='bold', color='white')
        ax.set_xlabel('Time', fontsize=12, color='white')
        ax.set_ylabel('Cumulative PnL (USDC)', fontsize=12, color='white')
        
        legend = ax.legend(fontsize=12)
        legend.get_frame().set_facecolor('#2a2a2a')
        legend.get_frame().set_edgecolor('white')
        for text in legend.get_texts():
            text.set_color('white')
        
        ax.grid(True, alpha=0.3, color='white')
        ax.tick_params(colors='white')
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(df_no_fees) // 10)))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='#1a1a1a')
            print(f"Plot saved to {output_file}")
        else:
            plt.show()
        
        return fig
    
    def run_comparison(self, l1_address: str, days_back: int = 30, output_file: str = None):
        """Run the complete PnL comparison analysis."""
        print(f"Analyzing PnL for address: {l1_address}")
        print(f"Generating sample data for last {days_back} days...")
        
        trades = self.get_sample_trades(l1_address, days_back)
        
        if not trades:
            print("No trade data found for the specified address and time range.")
            return
        
        pnl_no_fees, pnl_with_fees = self.get_pnl_with_fees(l1_address, trades)
        
        if not pnl_no_fees:
            print("No PnL data calculated.")
            return
        
        final_pnl_no_fees = pnl_no_fees[-1][1] if pnl_no_fees else 0
        final_pnl_with_fees = pnl_with_fees[-1][1] if pnl_with_fees else 0
        fee_impact = final_pnl_no_fees - final_pnl_with_fees
        
        print(f"\nSummary:")
        print(f"Final PnL (0% fees): ${final_pnl_no_fees:,.2f}")
        print(f"Final PnL (0.05% taker fees): ${final_pnl_with_fees:,.2f}")
        print(f"Total fee impact: ${fee_impact:,.2f}")
        print(f"Number of trades: {len(trades)}")
        
        fig = self.create_dual_plot(l1_address, pnl_no_fees, pnl_with_fees, output_file)
        return fig

def main():
    parser = argparse.ArgumentParser(description='Generate PnL comparison with and without taker fees')
    parser.add_argument('l1_address', help='L1 address to analyze')
    parser.add_argument('--days', type=int, default=30, help='Number of days to look back (default: 30)')
    parser.add_argument('--output', help='Output file path for the plot (optional)')
    
    args = parser.parse_args()
    
    try:
        comparison = PnLFeeComparison()
        comparison.run_comparison(args.l1_address, args.days, args.output)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
