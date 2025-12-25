# 📊 CẤU TRÚC & LUỒNG HOẠT ĐỘNG BOT

## 🏗️ Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────┐
│                     TELEGRAM USERS                          │
│              (Gửi lệnh & nhận tín hiệu)                     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   BOT.PY (Main Logic)                       │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Command Handlers: /start, /stop, /status, /stats    │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Periodic Job: Check signals every N seconds         │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────┬────────────────────────┬───────────────────┘
                 │                        │
                 ▼                        ▼
┌─────────────────────────┐   ┌──────────────────────────────┐
│  RSI_INDICATOR.PY       │   │  EXCHANGE_CLIENT.PY          │
│  ┌───────────────────┐  │   │  ┌────────────────────────┐  │
│  │ Calculate RSI     │  │   │  │ BinanceClient          │  │
│  │ Calculate EMA9    │  │   │  │  - Get BTC/USD data    │  │
│  │ Calculate WMA45   │  │   │  └────────────────────────┘  │
│  └───────────────────┘  │   │  ┌────────────────────────┐  │
│  ┌───────────────────┐  │   │  │ TwelveDataClient       │  │
│  │ 4-Step BUY Logic  │  │   │  │  - Get XAU/USD data    │  │
│  │ 4-Step SELL Logic │  │   │  └────────────────────────┘  │
│  └───────────────────┘  │   └──────────────┬───────────────┘
│  ┌───────────────────┐  │                  │
│  │ Signal Detection  │  │                  │
│  └───────────────────┘  │                  │
└─────────────────────────┘                  │
                                             ▼
                              ┌──────────────────────────────┐
                              │   EXTERNAL APIs              │
                              │  ┌────────────────────────┐  │
                              │  │ Binance API (Free)     │  │
                              │  │  - Real-time BTC data  │  │
                              │  └────────────────────────┘  │
                              │  ┌────────────────────────┐  │
                              │  │ Twelve Data API        │  │
                              │  │  - XAU/USD forex data  │  │
                              │  └────────────────────────┘  │
                              └──────────────────────────────┘
```

## 🔄 Luồng Xử Lý Tín Hiệu

```
START
  │
  ├─► [Every N seconds] Timer triggers check_signals()
  │
  ├─► For each Symbol (BTCUSD, XAUUSD):
  │     │
  │     ├─► For each Timeframe (15m, 1h):
  │     │     │
  │     │     ├─► Fetch price data (Klines)
  │     │     │     ├─ Binance API (if BTCUSD)
  │     │     │     └─ Twelve Data API (if XAUUSD)
  │     │     │
  │     │     ├─► Update indicator with new data
  │     │     │     ├─ Calculate RSI
  │     │     │     ├─ Calculate EMA9 of RSI
  │     │     │     ├─ Calculate WMA45 of RSI
  │     │     │     └─ Process 4-step logic
  │     │     │
  │     │     ├─► Check for new signals
  │     │     │     ├─ BUY #1? (RSI cross up EMA9)
  │     │     │     ├─ BUY #2? (RSI cross up WMA45)
  │     │     │     ├─ SELL #1? (RSI cross down EMA9)
  │     │     │     └─ SELL #2? (RSI cross down WMA45)
  │     │     │
  │     │     └─► If new signal detected:
  │     │           └─ Send alert to all subscribers
  │     │
  │     └─► Continue to next timeframe
  │
  └─► Loop continues...
```

## 📝 Chi Tiết 4 Bước Setup

### 🟢 BUY SETUP (Trend Reversal Down → Up)

```
Step 1: RSI ≥ 80 (Overbought)
   │
   ▼
Step 2: RSI crossunder EMA9
   │  (RSI giảm, cắt xuống dưới EMA9)
   ▼
Step 3: RSI crossunder WMA45
   │  (RSI tiếp tục giảm, cắt xuống dưới WMA45)
   ▼
Step 4: EMA9 crossunder WMA45
   │  (EMA9 cũng cắt xuống dưới WMA45)
   ▼
🟢 SETUP READY! (Sẵn sàng tín hiệu mua)
   │
   ├─► RSI cross up EMA9 (lần 2+) → BUY #1 ⚠️
   │
   └─► RSI cross up WMA45 → BUY #2 💪 (Reset)
```

### 🔴 SELL SETUP (Trend Reversal Up → Down)

```
Step 1: RSI ≤ 20 (Oversold)
   │
   ▼
Step 2: RSI crossover EMA9
   │  (RSI tăng, cắt lên trên EMA9)
   ▼
Step 3: RSI crossover WMA45
   │  (RSI tiếp tục tăng, cắt lên trên WMA45)
   ▼
Step 4: EMA9 crossover WMA45
   │  (EMA9 cũng cắt lên trên WMA45)
   ▼
🔴 SETUP READY! (Sẵn sàng tín hiệu bán)
   │
   ├─► RSI cross down EMA9 (lần 2+) → SELL #1 ⚠️
   │
   └─► RSI cross down WMA45 → SELL #2 💪 (Reset)
```

## 🎯 Ý Nghĩa Tín Hiệu

| Tín Hiệu | Độ Mạnh | Ý Nghĩa | Hành Động |
|----------|---------|---------|-----------|
| 🟢 BUY #1 | ⚠️ Thận trọng | RSI bắt đầu phục hồi sau downtrend | Entry thử nghiệm (position nhỏ) |
| 🟢 BUY #2 | 💪 Mạnh | RSI xác nhận uptrend, vượt WMA45 | Entry chính, add position |
| 🔴 SELL #1 | ⚠️ Thận trọng | RSI bắt đầu suy yếu sau uptrend | Take profit một phần |
| 🔴 SELL #2 | 💪 Mạnh | RSI xác nhận downtrend, phá WMA45 | Exit hoàn toàn, short |

## 📊 State Management

### BUY State Variables:
```python
buy_step1_touched_overbought    # True nếu đã chạm ≥80
buy_step2_crossed_ema9_down     # True nếu RSI đã cắt xuống EMA9
buy_step3_crossed_wma45_down    # True nếu RSI đã cắt xuống WMA45
buy_step4_ema9_crossed_wma45_down  # True nếu EMA9 đã cắt xuống WMA45
buy_rsi_ema9_cross_count        # Đếm số lần RSI cắt lên EMA9
buy_entry1_count                # Đếm số lần BUY #1 (max 2)
```

### SELL State Variables:
```python
sell_step1_touched_oversold     # True nếu đã chạm ≤20
sell_step2_crossed_ema9_up      # True nếu RSI đã cắt lên EMA9
sell_step3_crossed_wma45_up     # True nếu RSI đã cắt lên WMA45
sell_step4_ema9_crossed_wma45_up   # True nếu EMA9 đã cắt lên WMA45
sell_rsi_ema9_cross_count       # Đếm số lần RSI cắt xuống EMA9
sell_entry1_count               # Đếm số lần SELL #1 (max 2)
```

## 🔄 Reset Conditions

### BUY Setup Reset khi:
- Có tín hiệu BUY #2 (hoàn thành chu kỳ)
- RSI chạm vùng oversold (≤20) - chu kỳ bị gián đoạn

### SELL Setup Reset khi:
- Có tín hiệu SELL #2 (hoàn thành chu kỳ)
- RSI chạm vùng overbought (≥80) - chu kỳ bị gián đoạn

## ⚡ Performance & Optimization

### API Calls per Check:
```
2 symbols × 2 timeframes = 4 API calls/check

Example with CHECK_INTERVAL = 300s (5 min):
- Checks per day: 24h × 60min / 5min = 288
- API calls per day: 288 × 4 = 1,152 requests

Twelve Data Free Tier: 800 requests/day
→ Need to optimize! Use CHECK_INTERVAL ≥ 420s (7 min)
```

### Recommended Settings:
```python
# config.py
CHECK_INTERVAL = 420  # 7 minutes
# 205 checks/day × 4 = 820 requests/day ✅

# Or reduce to 1 timeframe per symbol:
TIMEFRAMES = ['1h']  # Only 1h
# 205 checks/day × 2 = 410 requests/day ✅✅
```

## 📦 Files & Responsibilities

| File | Trách Nhiệm |
|------|-------------|
| `bot.py` | Main logic, Telegram handlers, job scheduler |
| `rsi_indicator.py` | RSI calculation, signal detection, state management |
| `exchange_client.py` | Fetch data from Binance & Twelve Data |
| `config.py` | Configuration, environment variables |
| `requirements.txt` | Python dependencies |
| `Procfile` | Railway start command |
| `railway.json` | Railway deployment config |
| `setup.py` | Interactive setup wizard |

## 🎓 Giải Thích Logic Crossover

### Crossover vs Crossunder:

**Crossover** (Cắt lên):
```
prev: A < B
curr: A ≥ B
→ A vừa cắt LÊN B
```

**Crossunder** (Cắt xuống):
```
prev: A ≥ B
curr: A < B
→ A vừa cắt XUỐNG B
```

### Ví dụ thực tế:

```
Time  RSI   EMA9  Event
────────────────────────
t0:   45    50    (RSI dưới EMA9)
t1:   48    50    (RSI đang tăng)
t2:   52    50    (Crossover! RSI cắt lên EMA9)
t3:   55    51    (RSI trên EMA9)
t4:   48    52    (Crossunder! RSI cắt xuống EMA9)
```

## 🚦 Signal Flow Example

```
Scenario: BTC/USD 15m - BUY Setup

Hour 1: RSI = 85 → Step 1 ✓ (touched overbought)
Hour 2: RSI = 75, EMA9 = 78 → Step 2 ✓ (RSI cut down EMA9)
Hour 3: RSI = 65, WMA45 = 70 → Step 3 ✓ (RSI cut down WMA45)
Hour 4: EMA9 = 67, WMA45 = 68 → Step 4 ✓ (EMA9 cut down WMA45)

🟢 SETUP READY!

Hour 5: RSI = 55, EMA9 = 58 → Cross count = 1 (no signal yet)
Hour 6: RSI = 60, EMA9 = 58 → Cross count = 2 → 🟢 BUY #1 ⚠️
Hour 7: RSI = 62, EMA9 = 59 → (monitoring...)
Hour 8: RSI = 71, WMA45 = 68 → 🟢 BUY #2 💪 (Reset all states)
```

---

**Hiểu rõ logic → Sử dụng hiệu quả! 🎯**
