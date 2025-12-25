#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Setup Script
Helps you configure the bot before deployment
"""

import os
import sys

def main():
    print("=" * 60)
    print("🤖 RSI Trading Bot - Setup Wizard")
    print("=" * 60)
    print()
    
    # Check if .env exists
    env_exists = os.path.exists('.env')
    
    if env_exists:
        print("⚠️  File .env đã tồn tại!")
        response = input("Bạn có muốn cấu hình lại? (y/n): ")
        if response.lower() != 'y':
            print("Đã hủy setup.")
            return
    
    print("\n📋 Bước 1: Cấu hình Telegram Bot")
    print("-" * 60)
    print("Hướng dẫn lấy Bot Token:")
    print("1. Mở Telegram, tìm @BotFather")
    print("2. Gửi lệnh /newbot")
    print("3. Làm theo hướng dẫn để tạo bot")
    print("4. Copy Bot Token")
    print()
    
    telegram_token = input("Nhập TELEGRAM_BOT_TOKEN: ").strip()
    
    if not telegram_token:
        print("❌ Bot Token không được để trống!")
        return
    
    print("\n📋 Bước 2: Cấu hình Twelve Data API")
    print("-" * 60)
    print("Hướng dẫn lấy API Key:")
    print("1. Truy cập: https://twelvedata.com/")
    print("2. Đăng ký tài khoản miễn phí")
    print("3. Vào Dashboard và copy API Key")
    print("4. Free tier: 800 requests/day")
    print()
    
    twelve_data_key = input("Nhập TWELVE_DATA_API_KEY: ").strip()
    
    if not twelve_data_key:
        print("❌ API Key không được để trống!")
        return
    
    print("\n📋 Bước 3: Cấu hình tùy chọn")
    print("-" * 60)
    
    check_interval = input("Tần suất kiểm tra (giây) [mặc định: 300]: ").strip()
    if not check_interval:
        check_interval = "300"
    
    # Create .env file
    env_content = f"""# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN={telegram_token}

# Twelve Data API Key (for XAU/USD)
TWELVE_DATA_API_KEY={twelve_data_key}

# Bot Settings
CHECK_INTERVAL={check_interval}
LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("\n" + "=" * 60)
    print("✅ Setup hoàn tất!")
    print("=" * 60)
    print()
    print("📁 File .env đã được tạo với cấu hình:")
    print(f"   - Telegram Bot Token: {telegram_token[:10]}...")
    print(f"   - Twelve Data API Key: {twelve_data_key[:10]}...")
    print(f"   - Check Interval: {check_interval}s")
    print()
    print("📝 Các bước tiếp theo:")
    print("   1. Test bot local: python bot.py")
    print("   2. Deploy lên Railway (xem README.md)")
    print("   3. Thêm environment variables trên Railway")
    print()
    print("⚠️  LƯU Ý:")
    print("   - KHÔNG commit file .env vào Git")
    print("   - Trên Railway, dùng Variables tab để set env vars")
    print("   - Free tier Twelve Data: 800 requests/day")
    print("   - Khuyến nghị CHECK_INTERVAL >= 300s để tránh vượt limit")
    print()
    print("🚀 Good luck với bot của bạn!")
    print()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Đã hủy setup.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        sys.exit(1)
