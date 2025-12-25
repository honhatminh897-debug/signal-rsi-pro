# ⚡ HƯỚNG DẪN FIX LỖI BUILD NHANH

## ❌ Lỗi Bạn Gặp Phải

```
ModuleNotFoundError: No module named 'distutils'
exit code: 2
```

## ✅ NGUYÊN NHÂN

Railway dùng Python 3.12, nhưng `numpy==1.24.3` không tương thích.

## 🔧 CÁCH FIX (3 PHÚT)

### Option 1: Download Bản Đã Fix (Khuyến nghị)

👉 **[TẢI BẢN MỚI NHẤT (26 KB)](computer:///home/user/telegram-trading-bot.zip)**

Bản này đã fix tất cả lỗi build!

**Các thay đổi:**
- ✅ `requirements.txt` - Updated numpy & aiohttp
- ✅ `runtime.txt` - Chỉ định Python 3.11
- ✅ `nixpacks.toml` - Config build chính xác
- ✅ `FIXES.md` - Giải thích chi tiết

### Option 2: Fix Thủ Công

Nếu bạn đã upload code, chỉ cần update 3 files:

#### 1️⃣ Update `requirements.txt`
```python
python-telegram-bot==20.7
aiohttp==3.9.5
numpy==1.26.4
python-dotenv==1.0.0
```

#### 2️⃣ Tạo file `runtime.txt` (NEW)
```
python-3.11
```

#### 3️⃣ Tạo file `nixpacks.toml` (NEW)
```toml
[phases.setup]
nixPkgs = ["python311", "python311Packages.pip", "python311Packages.setuptools"]

[phases.install]
cmds = [
    "python3.11 -m venv --copies /opt/venv",
    ". /opt/venv/bin/activate && pip install --upgrade pip setuptools wheel",
    ". /opt/venv/bin/activate && pip install -r requirements.txt"
]

[start]
cmd = "python3.11 bot.py"
```

#### 4️⃣ Push changes
```bash
git add .
git commit -m "Fix Python 3.12 compatibility"
git push origin main
```

Railway sẽ tự động re-deploy!

## 🎯 KẾT QUẢ MONG ĐỢI

Build log sẽ show:
```
✅ Successfully installed numpy-1.26.4
✅ Successfully installed aiohttp-3.9.5
✅ Successfully installed python-telegram-bot-20.7
✅ Build completed successfully!
```

## 🚀 SAU KHI FIX

1. Railway tự động deploy lại
2. Check logs: Dashboard → Service → Logs
3. Verify bot chạy: "Bot started successfully!"
4. Test: Mở Telegram → `/start`

## 📋 FILES SUMMARY

**Bản mới có 16 files:**
```
Core (9):
- bot.py
- rsi_indicator.py
- exchange_client.py
- config.py
- requirements.txt (UPDATED)
- Procfile
- railway.json
- setup.py
- .gitignore

Build Config (3 NEW):
- runtime.txt
- nixpacks.toml
- FIXES.md

Documentation (4):
- README.md
- QUICKSTART.md
- ARCHITECTURE.md
- SUMMARY.md
```

## ⚠️ NẾU VẪN LỖI

### Try these:

**1. Force Python version trong Railway:**
```
Settings → Environment → Add Variable:
NIXPACKS_PYTHON_VERSION=3.11
```

**2. Clear build cache:**
```
Settings → Deployments → Latest → 3-dot menu → Redeploy
```

**3. Check logs chi tiết:**
```
Dashboard → Service → Logs → Filter: Error
```

## 📞 SUPPORT

Nếu vẫn gặp vấn đề:
1. Check file `FIXES.md` trong ZIP
2. Verify environment variables đã set
3. Check Railway logs để xem lỗi cụ thể

## ✅ CHECKLIST

- [ ] Download bản ZIP mới
- [ ] Upload lên GitHub (hoặc update files)
- [ ] Verify 3 files: requirements.txt, runtime.txt, nixpacks.toml
- [ ] Push changes
- [ ] Đợi Railway re-deploy
- [ ] Check logs thành công
- [ ] Test bot: /start

## 🎉 DONE!

Sau khi fix, bot sẽ chạy bình thường!

---

**👉 [DOWNLOAD BẢN ĐÃ FIX (26 KB)](computer:///home/user/telegram-trading-bot.zip)**

**Good luck! 🚀**
