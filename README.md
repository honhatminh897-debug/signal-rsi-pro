# 🤖 RSI Follow Trend Trading Bot

Bot Telegram tự động gửi tín hiệu trading dựa trên chỉ báo RSI Follow Trend.

## 📊 Tính Năng

- ✅ Theo dõi **BTC/USD** và **XAU/USD** (Vàng)
- ✅ Hỗ trợ timeframe **15m** và **1h**
- ✅ Logic 4 bước setup như Pine Script
- ✅ Tín hiệu BUY #1, BUY #2, SELL #1, SELL #2
- ✅ Thông báo real-time qua Telegram
- ✅ Xem trạng thái và thống kê

## 🚀 Hướng Dẫn Deploy Lên Railway

### Bước 1: Chuẩn Bị

#### 1.1. Tạo Telegram Bot
1. Mở Telegram, tìm **@BotFather**
2. Gửi lệnh `/newbot`
3. Đặt tên bot (ví dụ: RSI Trading Signal Bot)
4. Đặt username (ví dụ: rsi_trading_signal_bot)
5. Lưu lại **Bot Token** (dạng: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

#### 1.2. Lấy API Key Twelve Data (cho XAU/USD)
1. Truy cập: https://twelvedata.com/
2. Đăng ký tài khoản miễn phí
3. Vào Dashboard và copy **API Key**
4. Free tier: 800 requests/day (đủ dùng)

### Bước 2: Deploy Lên Railway

#### 2.1. Tạo Tài Khoản Railway
1. Truy cập: https://railway.app/
2. Đăng nhập bằng GitHub

#### 2.2. Deploy Bot

**Cách 1: Deploy từ GitHub (Khuyến nghị)**

1. Tạo repository GitHub mới
2. Upload tất cả files trong thư mục này lên repo
3. Vào Railway Dashboard
4. Click **New Project** → **Deploy from GitHub repo**
5. Chọn repository vừa tạo
6. Railway sẽ tự động build và deploy

**Cách 2: Deploy trực tiếp**

1. Vào Railway Dashboard
2. Click **New Project** → **Empty Project**
3. Click **Add Service** → **GitHub Repo**
4. Connect repository và deploy

#### 2.3. Cấu Hình Environment Variables

Sau khi deploy, vào **Variables** tab và thêm:

```
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TWELVE_DATA_API_KEY=your_twelve_data_api_key_here
LOG_LEVEL=INFO
```

**Quan trọng:** Thay các giá trị trên bằng token/key thật của bạn!

#### 2.4. Deploy

1. Click **Deploy** hoặc Railway sẽ tự động deploy khi có thay đổi
2. Đợi vài phút để build hoàn tất
3. Check logs để đảm bảo bot đã chạy

### Bước 3: Sử Dụng Bot

1. Mở Telegram và tìm bot của bạn (theo username đã đặt)
2. Gửi lệnh `/start` để bắt đầu
3. Bot sẽ tự động gửi thông báo khi có tín hiệu mới!

## 📱 Các Lệnh Bot

- `/start` - Bắt đầu nhận tín hiệu
- `/stop` - Dừng nhận tín hiệu
- `/status` - Xem trạng thái hiện tại (chọn symbol/timeframe)
- `/stats` - Xem thống kê tín hiệu
- `/help` - Hướng dẫn sử dụng

## 🎯 Logic Tín Hiệu

### Setup BUY (4 bước tuần tự):
1. RSI chạm vùng quá mua (≥80)
2. RSI cắt xuống EMA9
3. RSI cắt xuống WMA45
4. EMA9 cắt xuống WMA45
→ **Setup sẵn sàng**

**Tín hiệu vào lệnh:**
- **BUY #1** ⚠️: RSI cắt lên EMA9 (từ lần cắt thứ 2, tối đa 2 lần)
- **BUY #2** 💪: RSI cắt lên WMA45 (tín hiệu mạnh)

### Setup SELL (4 bước tuần tự):
1. RSI chạm vùng quá bán (≤20)
2. RSI cắt lên EMA9
3. RSI cắt lên WMA45
4. EMA9 cắt lên WMA45
→ **Setup sẵn sàng**

**Tín hiệu vào lệnh:**
- **SELL #1** ⚠️: RSI cắt xuống EMA9 (từ lần cắt thứ 2, tối đa 2 lần)
- **SELL #2** 💪: RSI cắt xuống WMA45 (tín hiệu mạnh)

## ⚙️ Tùy Chỉnh

Chỉnh sửa file `config.py` để thay đổi:

```python
# Các cặp trading
SYMBOLS = ['BTCUSD', 'XAUUSD']

# Timeframes
TIMEFRAMES = ['15m', '1h']

# Tần suất kiểm tra (giây)
CHECK_INTERVAL = 60

# Thông số RSI
RSI_LENGTH = 14
EMA_LENGTH = 9
WMA_LENGTH = 45
```

## 🔍 Kiểm Tra Logs

Trên Railway Dashboard:
1. Click vào service của bot
2. Vào tab **Deployments**
3. Click vào deployment đang chạy
4. Xem **Logs** để debug

## ⚠️ Lưu Ý

1. **Free Tier Railway**: 
   - $5 credit/month miễn phí
   - Đủ chạy bot 24/7

2. **Twelve Data Free Tier**:
   - 800 requests/day
   - Bot check mỗi 60s = 1440 checks/day
   - 2 symbols × 2 timeframes = 4 requests/check
   - Total: ~5760 requests/day → Cần nâng cấp hoặc tăng CHECK_INTERVAL

   **Giải pháp**: Đặt `CHECK_INTERVAL = 300` (5 phút) để giảm xuống ~1150 requests/day

3. **Data Source**:
   - BTC/USD: Từ Binance (miễn phí, không giới hạn)
   - XAU/USD: Từ Twelve Data (giới hạn free tier)

## 🐛 Troubleshooting

### Bot không chạy?
- Check logs trên Railway
- Verify TELEGRAM_BOT_TOKEN đúng
- Verify TWELVE_DATA_API_KEY đúng

### Không nhận tín hiệu?
- Gửi `/start` để đăng ký nhận tín hiệu
- Check logs xem bot có fetch data được không
- Verify API keys còn hạn

### Lỗi API limit?
- Tăng CHECK_INTERVAL trong config.py
- Hoặc nâng cấp Twelve Data plan

## 📝 File Structure

```
telegram-trading-bot/
├── bot.py                 # Main bot logic
├── rsi_indicator.py       # RSI calculation & signal logic
├── exchange_client.py     # Binance & Twelve Data clients
├── config.py              # Configuration
├── requirements.txt       # Python dependencies
├── Procfile              # Railway start command
├── railway.json          # Railway configuration
└── README.md             # Documentation
```

## 🔐 Bảo Mật

- **KHÔNG** commit API keys vào Git
- Luôn dùng Environment Variables
- File `.gitignore` đã được cấu hình

## 📞 Support

Nếu gặp vấn đề:
1. Check logs trên Railway
2. Verify các environment variables
3. Test API keys riêng lẻ

## 📄 License

MIT License - Free to use and modify

---

**Good luck with your trading! 🚀📈**

*Lưu ý: Đây chỉ là công cụ hỗ trợ, không phải lời khuyên đầu tư. Luôn cân nhắc rủi ro trước khi giao dịch.*
