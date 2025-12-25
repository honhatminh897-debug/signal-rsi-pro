# 🚀 HƯỚNG DẪN DEPLOY NHANH

## 📦 Các File Đã Tạo

Bot hoàn chỉnh gồm các file:

1. **bot.py** - Logic chính của bot
2. **rsi_indicator.py** - Tính toán RSI và logic tín hiệu
3. **exchange_client.py** - Kết nối Binance và Twelve Data
4. **config.py** - Cấu hình
5. **requirements.txt** - Dependencies Python
6. **Procfile** - Lệnh start cho Railway
7. **railway.json** - Cấu hình Railway
8. **setup.py** - Script setup nhanh (optional)
9. **README.md** - Hướng dẫn chi tiết

## ⚡ DEPLOY NHANH - 5 PHÚT

### Bước 1: Tạo Telegram Bot (2 phút)
1. Mở Telegram → tìm **@BotFather**
2. Gửi `/newbot`
3. Đặt tên: `RSI Trading Signal Bot`
4. Đặt username: `rsi_trading_signal_bot`
5. **LƯU LẠI TOKEN** (dạng: `123456:ABC-DEF...`)

### Bước 2: Lấy API Key Twelve Data (2 phút)
1. Truy cập: https://twelvedata.com/
2. Click **Sign Up** (đăng ký miễn phí)
3. Vào **Dashboard** → copy **API Key**
4. Free: 800 requests/day (đủ dùng)

### Bước 3: Deploy Lên Railway (1 phút)

#### Option A: Deploy từ GitHub (Khuyến nghị)
1. Tạo GitHub repo mới
2. Upload TẤT CẢ files trong folder `telegram-trading-bot`
3. Vào https://railway.app/ → Login with GitHub
4. **New Project** → **Deploy from GitHub repo**
5. Chọn repo vừa tạo
6. Vào **Variables** tab, thêm:
   ```
   TELEGRAM_BOT_TOKEN=paste_token_ở_đây
   TWELVE_DATA_API_KEY=paste_key_ở_đây
   ```
7. Railway tự động deploy!

#### Option B: Deploy trực tiếp CLI
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Init project
cd telegram-trading-bot
railway init

# Add environment variables
railway variables set TELEGRAM_BOT_TOKEN=your_token_here
railway variables set TWELVE_DATA_API_KEY=your_key_here

# Deploy
railway up
```

### Bước 4: Kiểm Tra Bot
1. Mở Telegram, tìm bot (theo username đã đặt)
2. Gửi `/start`
3. Bot reply → **THÀNH CÔNG!** 🎉

## 🎯 SỬ DỤNG BOT

### Lệnh cơ bản:
- `/start` - Bắt đầu nhận tín hiệu
- `/status` - Xem trạng thái (chọn symbol/timeframe)
- `/stats` - Xem thống kê tín hiệu
- `/help` - Hướng dẫn

### Tín hiệu sẽ nhận:
- 🟢 **BUY #1** - Tín hiệu mua thận trọng
- 🟢 **BUY #2** - Tín hiệu mua mạnh
- 🔴 **SELL #1** - Tín hiệu bán thận trọng
- 🔴 **SELL #2** - Tín hiệu bán mạnh

## ⚙️ ĐIỀU CHỈNH (Optional)

### Thay đổi tần suất kiểm tra:
Sửa file `config.py`:
```python
CHECK_INTERVAL = 300  # 5 phút (khuyến nghị cho free tier)
```

### Thêm cặp trading:
```python
SYMBOLS = ['BTCUSD', 'XAUUSD', 'ETHUSD']  # Thêm ETH
```

### Thay đổi timeframe:
```python
TIMEFRAMES = ['5m', '15m', '1h', '4h']  # Nhiều TF hơn
```

## ⚠️ LƯU Ý QUAN TRỌNG

### Railway Free Tier:
- ✅ $5 credit/month miễn phí
- ✅ Đủ chạy bot 24/7
- ✅ Không cần credit card

### Twelve Data Free Tier:
- ✅ 800 requests/day
- ⚠️ Bot check 60s = quá nhiều requests
- ✅ **GIẢI PHÁP**: Đặt `CHECK_INTERVAL = 300` (5 phút)
  - 2 symbols × 2 timeframes = 4 requests/check
  - 288 checks/day × 4 = 1152 requests
  - **CẦN OPTIMIZE**: Giảm xuống còn ~700 requests

### Optimization cho Free Tier:
```python
# Trong config.py
CHECK_INTERVAL = 360  # 6 phút = 240 checks/day
# 240 × 4 = 960 requests → Vẫn hơi cao

# KHUYẾN NGHỊ:
CHECK_INTERVAL = 420  # 7 phút = 205 checks/day  
# 205 × 4 = 820 requests → An toàn hơn
```

## 🐛 TROUBLESHOOTING

### Bot không chạy?
```bash
# Check logs trên Railway
# Dashboard → Service → Logs

# Kiểm tra:
1. TELEGRAM_BOT_TOKEN đúng chưa?
2. TWELVE_DATA_API_KEY đúng chưa?
3. Có lỗi trong logs không?
```

### Không nhận tín hiệu?
```
1. Gửi /start trong chat với bot
2. Check bot logs xem có fetch data không
3. Verify API keys còn hạn
```

### Lỗi "API limit exceeded"?
```python
# Tăng CHECK_INTERVAL trong config.py
CHECK_INTERVAL = 600  # 10 phút
```

## 📊 GIÁM SÁT

### Xem logs real-time:
Railway Dashboard → Service → **Logs** tab

### Check API usage:
- Twelve Data: https://twelvedata.com/account
- Xem số requests đã dùng

### Test bot:
```bash
# Local test (optional)
python setup.py  # Chạy setup wizard
python bot.py    # Test local
```

## 🔐 BẢO MẬT

- ❌ **KHÔNG** commit API keys vào Git
- ✅ Luôn dùng Environment Variables trên Railway
- ✅ File `.gitignore` đã được config sẵn

## 📞 HỖ TRỢ

Gặp vấn đề? Check:
1. **README.md** - Hướng dẫn đầy đủ
2. **Railway Logs** - Xem lỗi cụ thể
3. **Twelve Data Dashboard** - Check API usage

## 🎉 DONE!

Bot đã sẵn sàng! Mở Telegram và bắt đầu nhận tín hiệu! 🚀

---

**Chúc bạn trading thành công! 📈💰**
