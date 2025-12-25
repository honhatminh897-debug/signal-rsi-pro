#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration file for Trading Bot
"""

import os

# ============== TELEGRAM CONFIG ==============
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Admin chat IDs (optional - for admin notifications)
ADMIN_CHAT_IDS = [
    # Add admin Telegram user IDs here
    # Example: 123456789
]

# ============== API KEYS ==============
# Twelve Data API Key (for XAU/USD)
# Get free key at: https://twelvedata.com/
TWELVE_DATA_API_KEY = os.getenv('TWELVE_DATA_API_KEY', 'YOUR_TWELVE_DATA_API_KEY')

# ============== TRADING PAIRS ==============
SYMBOLS = ['BTCUSD', 'XAUUSD']

# ============== TIMEFRAMES ==============
TIMEFRAMES = ['15m', '1h']

# ============== INDICATOR SETTINGS ==============
RSI_LENGTH = 14
EMA_LENGTH = 9
WMA_LENGTH = 45

# ============== BOT SETTINGS ==============
# Check interval in seconds
CHECK_INTERVAL = 60  # Check every 60 seconds

# Number of candles to fetch for calculation
KLINE_LIMIT = 100

# ============== OVERBOUGHT/OVERSOLD LEVELS ==============
OVERBOUGHT_LEVEL = 80
OVERSOLD_LEVEL = 20

# ============== LOGGING ==============
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ============== RAILWAY SPECIFIC ==============
# Railway sets PORT environment variable
PORT = int(os.getenv('PORT', 8080))
