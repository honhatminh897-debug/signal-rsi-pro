#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram Trading Bot - RSI Follow Trend
Monitors BTC/USD and XAU/USD on 15m and 1h timeframes
"""

import os
import asyncio
import logging
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from rsi_indicator import RSIFollowTrend
from exchange_client import BinanceClient, TwelveDataClient
from config import (
    TELEGRAM_TOKEN, SYMBOLS, TIMEFRAMES, 
    CHECK_INTERVAL, ADMIN_CHAT_IDS
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TradingBot:
    def __init__(self):
        self.binance_client = BinanceClient()
        self.twelve_data_client = TwelveDataClient()
        self.indicators = {}
        self.subscribers = set()
        self.last_signals = {}
        
        # Initialize indicators for each symbol and timeframe
        for symbol in SYMBOLS:
            self.indicators[symbol] = {}
            for timeframe in TIMEFRAMES:
                key = f"{symbol}_{timeframe}"
                self.indicators[symbol][timeframe] = RSIFollowTrend()
                self.last_signals[key] = {
                    'buy_1': False,
                    'buy_2': False,
                    'sell_1': False,
                    'sell_2': False
                }
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /start command"""
        chat_id = update.effective_chat.id
        self.subscribers.add(chat_id)
        
        welcome_message = """
🤖 **RSI Follow Trend Bot**

Chào mừng! Bot sẽ theo dõi tín hiệu trading cho:
📊 **Symbols**: BTC/USD, XAU/USD
⏰ **Timeframes**: 15m, 1h

**Các lệnh:**
/start - Bắt đầu nhận tín hiệu
/stop - Dừng nhận tín hiệu
/status - Xem trạng thái hiện tại
/stats - Xem thống kê tín hiệu
/help - Hướng dẫn sử dụng

Bot đang chạy và sẽ gửi thông báo khi có tín hiệu mới! 🚀
        """
        await update.message.reply_text(welcome_message, parse_mode='Markdown')
    
    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /stop command"""
        chat_id = update.effective_chat.id
        if chat_id in self.subscribers:
            self.subscribers.remove(chat_id)
        await update.message.reply_text("✅ Đã dừng nhận tín hiệu. Dùng /start để bật lại.")
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /status command"""
        keyboard = [
            [InlineKeyboardButton("BTC/USD 15m", callback_data='status_BTCUSD_15m')],
            [InlineKeyboardButton("BTC/USD 1h", callback_data='status_BTCUSD_1h')],
            [InlineKeyboardButton("XAU/USD 15m", callback_data='status_XAUUSD_15m')],
            [InlineKeyboardButton("XAU/USD 1h", callback_data='status_XAUUSD_1h')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            '📊 Chọn cặp và timeframe để xem trạng thái:',
            reply_markup=reply_markup
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle button callbacks"""
        query = update.callback_query
        await query.answer()
        
        if query.data.startswith('status_'):
            parts = query.data.split('_')
            symbol = parts[1]
            timeframe = parts[2]
            
            status_msg = await self.get_status_message(symbol, timeframe)
            await query.edit_message_text(text=status_msg, parse_mode='Markdown')
    
    async def get_status_message(self, symbol: str, timeframe: str) -> str:
        """Generate status message for a symbol/timeframe"""
        try:
            indicator = self.indicators[symbol][timeframe]
            
            # Get current price
            if symbol == 'BTCUSD':
                price_data = await self.binance_client.get_price('BTCUSDT')
                price = price_data['price']
            else:  # XAUUSD
                price_data = await self.twelve_data_client.get_price('XAU/USD')
                price = price_data['price']
            
            status = indicator.get_status()
            
            msg = f"""
📊 **{symbol} - {timeframe}**
💰 Giá: ${price:,.2f}

**Chỉ báo:**
RSI: {status['rsi']:.2f}
EMA9: {status['ema9']:.2f}
WMA45: {status['wma45']:.2f}

**🟢 BUY SETUP:**
{'✓' if status['buy_step1'] else '○'} Bước 1: RSI≥80
{'✓' if status['buy_step2'] else '○'} Bước 2: RSI↓EMA9
{'✓' if status['buy_step3'] else '○'} Bước 3: RSI↓WMA45
{'✓' if status['buy_step4'] else '○'} Bước 4: EMA9↓WMA45
Status: {'🟢 READY!' if status['buy_setup_ready'] else '⏳ Chờ...'}
Crosses: {status['buy_cross_count']}
Entry #1: {status['buy_entry1_count']}/2

**🔴 SELL SETUP:**
{'✓' if status['sell_step1'] else '○'} Bước 1: RSI≤20
{'✓' if status['sell_step2'] else '○'} Bước 2: RSI↑EMA9
{'✓' if status['sell_step3'] else '○'} Bước 3: RSI↑WMA45
{'✓' if status['sell_step4'] else '○'} Bước 4: EMA9↑WMA45
Status: {'🔴 READY!' if status['sell_setup_ready'] else '⏳ Chờ...'}
Crosses: {status['sell_cross_count']}
Entry #1: {status['sell_entry1_count']}/2

⏰ Cập nhật: {datetime.now().strftime('%H:%M:%S')}
            """
            return msg
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            return f"❌ Lỗi khi lấy dữ liệu cho {symbol} {timeframe}"
    
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /stats command"""
        msg = "📈 **Thống Kê Tín Hiệu**\n\n"
        
        for symbol in SYMBOLS:
            msg += f"**{symbol}:**\n"
            for timeframe in TIMEFRAMES:
                indicator = self.indicators[symbol][timeframe]
                stats = indicator.get_statistics()
                msg += f"  {timeframe}: BUY#1={stats['total_buy_1']}, BUY#2={stats['total_buy_2']}, "
                msg += f"SELL#1={stats['total_sell_1']}, SELL#2={stats['total_sell_2']}\n"
            msg += "\n"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler for /help command"""
        help_text = """
📚 **Hướng Dẫn Sử Dụng Bot**

**Tín hiệu giao dịch:**
🟢 **BUY #1**: Tín hiệu mua thận trọng (từ lần cắt thứ 2)
🟢 **BUY #2**: Tín hiệu mua mạnh (cắt WMA45)
🔴 **SELL #1**: Tín hiệu bán thận trọng (từ lần cắt thứ 2)
🔴 **SELL #2**: Tín hiệu bán mạnh (cắt WMA45)

**Logic 4 bước:**
Setup BUY: RSI≥80 → RSI↓EMA9 → RSI↓WMA45 → EMA9↓WMA45
Setup SELL: RSI≤20 → RSI↑EMA9 → RSI↑WMA45 → EMA9↑WMA45

**Lưu ý:**
- Setup phải hoàn thành đủ 4 bước theo thứ tự
- Tín hiệu #1 xuất hiện từ lần cắt thứ 2 trở đi
- Mỗi setup chỉ cho tối đa 2 tín hiệu #1
- Tín hiệu #2 mạnh hơn và kết thúc chu kỳ

**Các lệnh:**
/start - Bắt đầu bot
/stop - Dừng nhận tín hiệu
/status - Trạng thái hiện tại
/stats - Thống kê tín hiệu
/help - Hiển thị hướng dẫn này
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def check_signals(self, context: ContextTypes.DEFAULT_TYPE):
        """Periodic task to check for new signals"""
        try:
            for symbol in SYMBOLS:
                for timeframe in TIMEFRAMES:
                    await self.process_symbol(symbol, timeframe, context)
        except Exception as e:
            logger.error(f"Error in check_signals: {e}")
    
    async def process_symbol(self, symbol: str, timeframe: str, context: ContextTypes.DEFAULT_TYPE):
        """Process a single symbol/timeframe combination"""
        try:
            # Get price data
            if symbol == 'BTCUSD':
                klines = await self.binance_client.get_klines('BTCUSDT', timeframe, limit=100)
            else:  # XAUUSD
                klines = await self.twelve_data_client.get_klines('XAU/USD', timeframe, limit=100)
            
            if not klines:
                return
            
            # Update indicator
            indicator = self.indicators[symbol][timeframe]
            indicator.update(klines)
            
            # Check for new signals
            signals = indicator.get_signals()
            key = f"{symbol}_{timeframe}"
            
            # Check BUY #1
            if signals['buy_1'] and not self.last_signals[key]['buy_1']:
                await self.send_signal_alert(context, symbol, timeframe, 'BUY #1', klines[-1]['close'])
                self.last_signals[key]['buy_1'] = True
            elif not signals['buy_1']:
                self.last_signals[key]['buy_1'] = False
            
            # Check BUY #2
            if signals['buy_2'] and not self.last_signals[key]['buy_2']:
                await self.send_signal_alert(context, symbol, timeframe, 'BUY #2', klines[-1]['close'])
                self.last_signals[key]['buy_2'] = True
            elif not signals['buy_2']:
                self.last_signals[key]['buy_2'] = False
            
            # Check SELL #1
            if signals['sell_1'] and not self.last_signals[key]['sell_1']:
                await self.send_signal_alert(context, symbol, timeframe, 'SELL #1', klines[-1]['close'])
                self.last_signals[key]['sell_1'] = True
            elif not signals['sell_1']:
                self.last_signals[key]['sell_1'] = False
            
            # Check SELL #2
            if signals['sell_2'] and not self.last_signals[key]['sell_2']:
                await self.send_signal_alert(context, symbol, timeframe, 'SELL #2', klines[-1]['close'])
                self.last_signals[key]['sell_2'] = True
            elif not signals['sell_2']:
                self.last_signals[key]['sell_2'] = False
            
        except Exception as e:
            logger.error(f"Error processing {symbol} {timeframe}: {e}")
    
    async def send_signal_alert(self, context: ContextTypes.DEFAULT_TYPE, 
                                symbol: str, timeframe: str, signal_type: str, price: float):
        """Send signal alert to all subscribers"""
        indicator = self.indicators[symbol][timeframe]
        status = indicator.get_status()
        
        emoji = '🟢' if 'BUY' in signal_type else '🔴'
        strength = '💪 MẠNH' if '#2' in signal_type else '⚠️ THẬN TRỌNG'
        
        message = f"""
{emoji} **TÍN HIỆU {signal_type}** {emoji}

📊 **{symbol}** | ⏰ **{timeframe}**
💰 Giá: ${price:,.2f}

**Độ mạnh:** {strength}

**Chỉ báo:**
RSI: {status['rsi']:.2f}
EMA9: {status['ema9']:.2f}
WMA45: {status['wma45']:.2f}

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        # Send to all subscribers
        for chat_id in self.subscribers:
            try:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Error sending message to {chat_id}: {e}")

def main():
    """Main function to run the bot"""
    # Create bot instance
    bot = TradingBot()
    
    # Create application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Add command handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("stop", bot.stop))
    application.add_handler(CommandHandler("status", bot.status))
    application.add_handler(CommandHandler("stats", bot.stats))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    
    # Add periodic job to check signals
    job_queue = application.job_queue
    job_queue.run_repeating(bot.check_signals, interval=CHECK_INTERVAL, first=10)
    
    # Start the bot
    logger.info("Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
