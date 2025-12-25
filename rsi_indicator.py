#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSI Follow Trend Indicator
Based on Pine Script logic with 4-step setup
"""

import numpy as np
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class RSIFollowTrend:
    def __init__(self, rsi_length: int = 14, ema_length: int = 9, wma_length: int = 45):
        self.rsi_length = rsi_length
        self.ema_length = ema_length
        self.wma_length = wma_length
        
        # State variables for BUY logic
        self.buy_step1_touched_overbought = False
        self.buy_step2_crossed_ema9_down = False
        self.buy_step3_crossed_wma45_down = False
        self.buy_step4_ema9_crossed_wma45_down = False
        self.buy_rsi_ema9_cross_count = 0
        self.buy_entry1_count = 0
        
        # State variables for SELL logic
        self.sell_step1_touched_oversold = False
        self.sell_step2_crossed_ema9_up = False
        self.sell_step3_crossed_wma45_up = False
        self.sell_step4_ema9_crossed_wma45_up = False
        self.sell_rsi_ema9_cross_count = 0
        self.sell_entry1_count = 0
        
        # Statistics
        self.total_buy_1 = 0
        self.total_buy_2 = 0
        self.total_sell_1 = 0
        self.total_sell_2 = 0
        
        # Previous values for crossover detection
        self.prev_rsi = None
        self.prev_ema9 = None
        self.prev_wma45 = None
        
        # Current values
        self.current_rsi = None
        self.current_ema9 = None
        self.current_wma45 = None
    
    def calculate_rsi(self, prices: np.ndarray, period: int) -> float:
        """Calculate RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_ema(self, values: np.ndarray, period: int) -> float:
        """Calculate EMA"""
        if len(values) < period:
            return np.mean(values)
        
        multiplier = 2 / (period + 1)
        ema = values[0]
        
        for value in values[1:]:
            ema = (value * multiplier) + (ema * (1 - multiplier))
        
        return ema
    
    def calculate_wma(self, values: np.ndarray, period: int) -> float:
        """Calculate WMA (Weighted Moving Average)"""
        if len(values) < period:
            return np.mean(values)
        
        weights = np.arange(1, period + 1)
        wma = np.sum(values[-period:] * weights) / np.sum(weights)
        return wma
    
    def update(self, klines: List[Dict]):
        """Update indicator with new kline data"""
        try:
            # Extract closing prices
            closes = np.array([float(k['close']) for k in klines])
            
            if len(closes) < max(self.rsi_length, self.ema_length, self.wma_length) + 10:
                logger.warning("Not enough data to calculate indicators")
                return
            
            # Calculate RSI
            rsi_values = []
            for i in range(self.rsi_length, len(closes)):
                rsi = self.calculate_rsi(closes[:i+1], self.rsi_length)
                rsi_values.append(rsi)
            
            rsi_array = np.array(rsi_values)
            
            # Store previous values
            self.prev_rsi = self.current_rsi
            self.prev_ema9 = self.current_ema9
            self.prev_wma45 = self.current_wma45
            
            # Calculate current values
            self.current_rsi = rsi_array[-1]
            self.current_ema9 = self.calculate_ema(rsi_array, self.ema_length)
            self.current_wma45 = self.calculate_wma(rsi_array, self.wma_length)
            
            # Only process if we have previous values
            if self.prev_rsi is None:
                return
            
            # Process BUY logic
            self._process_buy_logic()
            
            # Process SELL logic
            self._process_sell_logic()
            
        except Exception as e:
            logger.error(f"Error updating indicator: {e}")
    
    def _process_buy_logic(self):
        """Process BUY signal logic"""
        # Step 1: RSI touched overbought
        if self.current_rsi >= 80:
            self.buy_step1_touched_overbought = True
        
        # Step 2: RSI crossunder EMA9
        if (self.buy_step1_touched_overbought and 
            self.prev_rsi >= self.prev_ema9 and 
            self.current_rsi < self.current_ema9):
            self.buy_step2_crossed_ema9_down = True
        
        # Step 3: RSI crossunder WMA45
        if (self.buy_step2_crossed_ema9_down and 
            self.prev_rsi >= self.prev_wma45 and 
            self.current_rsi < self.current_wma45):
            self.buy_step3_crossed_wma45_down = True
        
        # Step 4: EMA9 crossunder WMA45
        if (self.buy_step3_crossed_wma45_down and 
            self.prev_ema9 >= self.prev_wma45 and 
            self.current_ema9 < self.current_wma45):
            self.buy_step4_ema9_crossed_wma45_down = True
        
        # Setup ready
        buy_setup_ready = self.buy_step4_ema9_crossed_wma45_down
        
        # Count crossovers after setup ready
        if (buy_setup_ready and 
            self.prev_rsi < self.prev_ema9 and 
            self.current_rsi >= self.current_ema9):
            self.buy_rsi_ema9_cross_count += 1
        
        # Check for BUY #2 signal (RSI crossover WMA45)
        buy_2 = (buy_setup_ready and 
                 self.prev_rsi < self.prev_wma45 and 
                 self.current_rsi >= self.current_wma45)
        
        if buy_2:
            self.total_buy_2 += 1
            self._reset_buy_state()
        
        # Reset if RSI touches oversold
        if self.current_rsi <= 20:
            self._reset_buy_state()
    
    def _process_sell_logic(self):
        """Process SELL signal logic"""
        # Step 1: RSI touched oversold
        if self.current_rsi <= 20:
            self.sell_step1_touched_oversold = True
        
        # Step 2: RSI crossover EMA9
        if (self.sell_step1_touched_oversold and 
            self.prev_rsi <= self.prev_ema9 and 
            self.current_rsi > self.current_ema9):
            self.sell_step2_crossed_ema9_up = True
        
        # Step 3: RSI crossover WMA45
        if (self.sell_step2_crossed_ema9_up and 
            self.prev_rsi <= self.prev_wma45 and 
            self.current_rsi > self.current_wma45):
            self.sell_step3_crossed_wma45_up = True
        
        # Step 4: EMA9 crossover WMA45
        if (self.sell_step3_crossed_wma45_up and 
            self.prev_ema9 <= self.prev_wma45 and 
            self.current_ema9 > self.current_wma45):
            self.sell_step4_ema9_crossed_wma45_up = True
        
        # Setup ready
        sell_setup_ready = self.sell_step4_ema9_crossed_wma45_up
        
        # Count crossovers after setup ready
        if (sell_setup_ready and 
            self.prev_rsi > self.prev_ema9 and 
            self.current_rsi <= self.current_ema9):
            self.sell_rsi_ema9_cross_count += 1
        
        # Check for SELL #2 signal (RSI crossunder WMA45)
        sell_2 = (sell_setup_ready and 
                  self.prev_rsi > self.prev_wma45 and 
                  self.current_rsi <= self.current_wma45)
        
        if sell_2:
            self.total_sell_2 += 1
            self._reset_sell_state()
        
        # Reset if RSI touches overbought
        if self.current_rsi >= 80:
            self._reset_sell_state()
    
    def _reset_buy_state(self):
        """Reset BUY state variables"""
        self.buy_step1_touched_overbought = False
        self.buy_step2_crossed_ema9_down = False
        self.buy_step3_crossed_wma45_down = False
        self.buy_step4_ema9_crossed_wma45_down = False
        self.buy_rsi_ema9_cross_count = 0
        self.buy_entry1_count = 0
    
    def _reset_sell_state(self):
        """Reset SELL state variables"""
        self.sell_step1_touched_oversold = False
        self.sell_step2_crossed_ema9_up = False
        self.sell_step3_crossed_wma45_up = False
        self.sell_step4_ema9_crossed_wma45_up = False
        self.sell_rsi_ema9_cross_count = 0
        self.sell_entry1_count = 0
    
    def get_signals(self) -> Dict[str, bool]:
        """Get current signals"""
        if self.current_rsi is None or self.prev_rsi is None:
            return {
                'buy_1': False,
                'buy_2': False,
                'sell_1': False,
                'sell_2': False
            }
        
        buy_setup_ready = self.buy_step4_ema9_crossed_wma45_down
        sell_setup_ready = self.sell_step4_ema9_crossed_wma45_up
        
        # BUY #1: RSI crossover EMA9 from 2nd cross onwards (max 2 times)
        buy_1 = (buy_setup_ready and 
                 self.buy_rsi_ema9_cross_count >= 2 and 
                 self.buy_entry1_count < 2 and
                 self.prev_rsi < self.prev_ema9 and 
                 self.current_rsi >= self.current_ema9)
        
        if buy_1:
            self.buy_entry1_count += 1
            self.total_buy_1 += 1
        
        # BUY #2: RSI crossover WMA45
        buy_2 = (buy_setup_ready and 
                 self.prev_rsi < self.prev_wma45 and 
                 self.current_rsi >= self.current_wma45)
        
        # SELL #1: RSI crossunder EMA9 from 2nd cross onwards (max 2 times)
        sell_1 = (sell_setup_ready and 
                  self.sell_rsi_ema9_cross_count >= 2 and 
                  self.sell_entry1_count < 2 and
                  self.prev_rsi > self.prev_ema9 and 
                  self.current_rsi <= self.current_ema9)
        
        if sell_1:
            self.sell_entry1_count += 1
            self.total_sell_1 += 1
        
        # SELL #2: RSI crossunder WMA45
        sell_2 = (sell_setup_ready and 
                  self.prev_rsi > self.prev_wma45 and 
                  self.current_rsi <= self.current_wma45)
        
        return {
            'buy_1': buy_1,
            'buy_2': buy_2,
            'sell_1': sell_1,
            'sell_2': sell_2
        }
    
    def get_status(self) -> Dict:
        """Get current indicator status"""
        return {
            'rsi': self.current_rsi if self.current_rsi else 50.0,
            'ema9': self.current_ema9 if self.current_ema9 else 50.0,
            'wma45': self.current_wma45 if self.current_wma45 else 50.0,
            'buy_step1': self.buy_step1_touched_overbought,
            'buy_step2': self.buy_step2_crossed_ema9_down,
            'buy_step3': self.buy_step3_crossed_wma45_down,
            'buy_step4': self.buy_step4_ema9_crossed_wma45_down,
            'buy_setup_ready': self.buy_step4_ema9_crossed_wma45_down,
            'buy_cross_count': self.buy_rsi_ema9_cross_count,
            'buy_entry1_count': self.buy_entry1_count,
            'sell_step1': self.sell_step1_touched_oversold,
            'sell_step2': self.sell_step2_crossed_ema9_up,
            'sell_step3': self.sell_step3_crossed_wma45_up,
            'sell_step4': self.sell_step4_ema9_crossed_wma45_up,
            'sell_setup_ready': self.sell_step4_ema9_crossed_wma45_up,
            'sell_cross_count': self.sell_rsi_ema9_cross_count,
            'sell_entry1_count': self.sell_entry1_count,
        }
    
    def get_statistics(self) -> Dict:
        """Get signal statistics"""
        return {
            'total_buy_1': self.total_buy_1,
            'total_buy_2': self.total_buy_2,
            'total_sell_1': self.total_sell_1,
            'total_sell_2': self.total_sell_2,
        }
