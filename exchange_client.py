#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Exchange clients for fetching price data
Supports Binance (for BTC/USD) and Twelve Data (for XAU/USD)
"""

import aiohttp
import logging
from typing import List, Dict, Optional
from datetime import datetime
from config import TWELVE_DATA_API_KEY

logger = logging.getLogger(__name__)

class BinanceClient:
    """Client for Binance API"""
    
    BASE_URL = "https://api.binance.com/api/v3"
    
    def __init__(self):
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def get_klines(self, symbol: str, interval: str, limit: int = 100) -> List[Dict]:
        """
        Get candlestick data from Binance
        
        Args:
            symbol: Trading pair (e.g., 'BTCUSDT')
            interval: Timeframe (e.g., '15m', '1h')
            limit: Number of candles to fetch
        
        Returns:
            List of kline dictionaries
        """
        try:
            session = await self._get_session()
            url = f"{self.BASE_URL}/klines"
            params = {
                'symbol': symbol,
                'interval': interval,
                'limit': limit
            }
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Binance API error: {response.status}")
                    return []
                
                data = await response.json()
                
                # Convert to standard format
                klines = []
                for k in data:
                    klines.append({
                        'timestamp': k[0],
                        'open': float(k[1]),
                        'high': float(k[2]),
                        'low': float(k[3]),
                        'close': float(k[4]),
                        'volume': float(k[5])
                    })
                
                return klines
                
        except Exception as e:
            logger.error(f"Error fetching Binance klines: {e}")
            return []
    
    async def get_price(self, symbol: str) -> Dict:
        """Get current price for a symbol"""
        try:
            session = await self._get_session()
            url = f"{self.BASE_URL}/ticker/price"
            params = {'symbol': symbol}
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Binance API error: {response.status}")
                    return {'price': 0.0}
                
                data = await response.json()
                return {'price': float(data['price'])}
                
        except Exception as e:
            logger.error(f"Error fetching Binance price: {e}")
            return {'price': 0.0}
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()


class TwelveDataClient:
    """Client for Twelve Data API (for forex and commodities)"""
    
    BASE_URL = "https://api.twelvedata.com"
    
    def __init__(self):
        self.api_key = TWELVE_DATA_API_KEY
        self.session = None
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _convert_interval(self, interval: str) -> str:
        """Convert interval format to Twelve Data format"""
        # Binance format to Twelve Data format
        mapping = {
            '1m': '1min',
            '5m': '5min',
            '15m': '15min',
            '30m': '30min',
            '1h': '1h',
            '4h': '4h',
            '1d': '1day'
        }
        return mapping.get(interval, interval)
    
    async def get_klines(self, symbol: str, interval: str, limit: int = 100) -> List[Dict]:
        """
        Get candlestick data from Twelve Data
        
        Args:
            symbol: Trading pair (e.g., 'XAU/USD')
            interval: Timeframe (e.g., '15m', '1h')
            limit: Number of candles to fetch
        
        Returns:
            List of kline dictionaries
        """
        try:
            if not self.api_key:
                logger.error("Twelve Data API key not configured")
                return []
            
            session = await self._get_session()
            url = f"{self.BASE_URL}/time_series"
            
            params = {
                'symbol': symbol,
                'interval': self._convert_interval(interval),
                'outputsize': limit,
                'apikey': self.api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Twelve Data API error: {response.status}")
                    return []
                
                data = await response.json()
                
                if 'values' not in data:
                    logger.error(f"Unexpected Twelve Data response: {data}")
                    return []
                
                # Convert to standard format
                klines = []
                for v in reversed(data['values']):  # Reverse to get chronological order
                    klines.append({
                        'timestamp': int(datetime.strptime(v['datetime'], '%Y-%m-%d %H:%M:%S').timestamp() * 1000),
                        'open': float(v['open']),
                        'high': float(v['high']),
                        'low': float(v['low']),
                        'close': float(v['close']),
                        'volume': float(v.get('volume', 0))
                    })
                
                return klines
                
        except Exception as e:
            logger.error(f"Error fetching Twelve Data klines: {e}")
            return []
    
    async def get_price(self, symbol: str) -> Dict:
        """Get current price for a symbol"""
        try:
            if not self.api_key:
                logger.error("Twelve Data API key not configured")
                return {'price': 0.0}
            
            session = await self._get_session()
            url = f"{self.BASE_URL}/price"
            
            params = {
                'symbol': symbol,
                'apikey': self.api_key
            }
            
            async with session.get(url, params=params) as response:
                if response.status != 200:
                    logger.error(f"Twelve Data API error: {response.status}")
                    return {'price': 0.0}
                
                data = await response.json()
                
                if 'price' not in data:
                    logger.error(f"Unexpected Twelve Data response: {data}")
                    return {'price': 0.0}
                
                return {'price': float(data['price'])}
                
        except Exception as e:
            logger.error(f"Error fetching Twelve Data price: {e}")
            return {'price': 0.0}
    
    async def close(self):
        """Close the session"""
        if self.session and not self.session.closed:
            await self.session.close()


# Example usage for testing
if __name__ == '__main__':
    import asyncio
    
    async def test_clients():
        # Test Binance
        binance = BinanceClient()
        print("Testing Binance...")
        klines = await binance.get_klines('BTCUSDT', '15m', 10)
        print(f"Got {len(klines)} klines from Binance")
        if klines:
            print(f"Last close: {klines[-1]['close']}")
        
        price = await binance.get_price('BTCUSDT')
        print(f"Current BTC price: {price['price']}")
        
        await binance.close()
        
        # Test Twelve Data
        twelve = TwelveDataClient()
        print("\nTesting Twelve Data...")
        klines = await twelve.get_klines('XAU/USD', '15m', 10)
        print(f"Got {len(klines)} klines from Twelve Data")
        if klines:
            print(f"Last close: {klines[-1]['close']}")
        
        price = await twelve.get_price('XAU/USD')
        print(f"Current XAU price: {price['price']}")
        
        await twelve.close()
    
    asyncio.run(test_clients())
