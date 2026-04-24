import requests
import os
from datetime import datetime

# Cấu hình Telegram Bot
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', "8727925469:AAGDq2pNNekunJInbLVi9akdcri7zav-sfY")
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 8114628397)

# File để lưu số dư cũ
BALANCE_FILE = "last_balance.txt"
# File để kiểm tra đã gửi thông báo bắt đầu chưa
STARTUP_FILE = "startup_sent.txt"

def send_telegram_message(message):
    """Gửi thông báo qua Telegram"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"  ❌ Lỗi gửi Telegram: {e}")
        return False

def get_user_data():
    """Lấy dữ liệu người dùng từ API"""
    url = "https://www.locgoh5.top/vn-app-server/app/v1/user/personalHomepage"
    
    headers = {
        "accept": "*/*",
        "accept-language": "vi-VN",
        "authorization": "Bearer_eyJ0eXBlIjoiSldUIiwiYWxnIjoiSFM1MTIifQ.eyJqdGkiOiJyUVJrJHlOOjclKkJ3fUwtVU5ILVBPPVdFVy1YRi1dTX40Izt5R2E6YV9GeyIsImlzcyI6InBheW1lbnQiLCJwaG9uZSI6IjM4NTE3ODA3MCIsInVzZXJObyI6IkFVTjAwMDAwMDAwMDAwMjY1NSIsImxvZ2luTmFtZSI6ImNvbm1lb2N1dGUiLCJpZCI6MjYwOSwicGF5Q29kZSI6IlZOIiwiZGV2aWNlSWQiOiJDUUtHQVFWQjdZWEUiLCJpbnZpdGF0aW9uQ29kZSI6IkNRSlJPSiIsInN1YiI6IkFVTjAwMDAwMDAwMDAwMjY1NSIsImlhdCI6MTc3Njk1NTQzOCwiZXhwIjoxODA4NDkxNDM4fQ.7G3XN8FhsTXOtlSgAi0v1k7OVpwRUrxRnxpL2l8_Jr-RaAXpMpZQMqrUFreCnuRoQc0O79_JCrzJz-O8YGoAlQ",
        "client-platform": "H5",
        "content-type": "application/json",
        "deviceid": "CQKGAQVB7YXE",
        "origin": "https://h5.locgoh5.top",
        "referer": "https://h5.locgoh5.top/",
        "request-paycode": "VN",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        response = requests.post(url, headers=headers, json={}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "0":
                user_data = data["data"]
                nickname = user_data.get("nickName", "N/A")
                income = int(float(user_data.get("income", 0)))
                return nickname, income
            else:
                print(f"  ❌ API lỗi: {data.get('msg')}")
                return None, None
        else:
            print(f"  ❌ HTTP {response.status_code}")
            return None, None
    except Exception as e:
        print(f"  ❌ Lỗi kết nối: {e}")
        return None, None

def format_money(amount):
    """Format số tiền với dấu chấm phân cách"""
    return f"{amount:,} VND".replace(",", ".")

def read_last_balance():
    """Đọc số dư lần trước từ file"""
    try:
        with open(BALANCE_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return None

def save_last_balance(balance):
    """Lưu số dư hiện tại vào file"""
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def should_send_startup_message():
    """Kiểm tra đã gửi thông báo bắt đầu chưa"""
    try:
        with open(STARTUP_FILE, 'r') as f:
            return False  # Đã gửi rồi
    except:
        return True  # Chưa gửi

def mark_startup_sent():
    """Đánh dấu đã gửi thông báo bắt đầu"""
    with open(STARTUP_FILE, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def main():
    """Chạy kiểm tra 1 lần (mỗi lần GitHub Actions gọi)"""
    # Lấy thời gian hiện tại và nickname
    current_time = datetime.now().strftime('%H:%M:%S')
    
    # Lấy thông tin người dùng để tag tên
    nickname, _ = get_user_data()
    if nickname is None:
        nickname = "conmeocute"
    
    # Gửi thông báo bắt đầu (chỉ 1 lần duy nhất)
    if should_send_startup_message():
        startup_message = f"🚀 <b>BOT ĐÃ BẮT ĐẦU CHẠY</b> 🚀\n\n"
        startup_message += f"👤 @{nickname}\n"
        startup_message += f"⏱️  Kiểm tra mỗi <b>5 phút</b>\n"
        startup_message += f"📊 Đang theo dõi biến động số dư..."
        
        if send_telegram_message(startup_message):
            mark_startup_sent()
            print("  ✅ Đã gửi thông báo bắt đầu")
        else:
            print("  ❌ Gửi thông báo bắt đầu thất bại")
    
    # In tiêu đề
    print("=" * 50)
    print("   THEO DÕI BIẾN ĐỘNG SỐ DƯ")
    print("=" * 50)
    print(f"📱 Telegram: @zenitsu2006z")
    print(f"⏱️  Cập nhật: mỗi 5 phút (GitHub Actions)")
    print("=" * 50)
    print()
    
    # Lấy dữ liệu
    nickname, current_balance = get_user_data()
    
    if current_balance is not None:
        # Hiển thị dòng thông tin
        display_line = f"[{current_time}] 👤 {nickname} | 💰 {format_money(current_balance)}"
        print(display_line)
        
        # Lấy số dư cũ từ file
        last_balance = read_last_balance()
        
        # Lưu số dư hiện tại
        save_last_balance(current_balance)
        
        # Kiểm tra biến động
        if last_balance is not None and current_balance != last_balance:
            change = current_balance - last_balance
            change_symbol = "+" if change > 0 else ""
            
            # In thông báo biến động
            print(f"  ⚡ BIẾN ĐỘNG: {change_symbol}{format_money(abs(change))}")
            
            # Tin nhắn Telegram - 3 DÒNG
            message = f"👤 @{nickname}\n"
            message += f"💰 Số dư hiện tại: {format_money(current_balance)}\n"
            message += f"🔄 Chênh lệch: {change_symbol}{format_money(abs(change))}"
            
            if send_telegram_message(message):
                print("  ✅ Đã gửi thông báo Telegram")
            else:
                print("  ❌ Gửi thông báo thất bại")
        elif last_balance is None:
            print("  📝 Lần đầu chạy, đã lưu số dư hiện tại")
        else:
            print("  ✅ Không có biến động")
    else:
        print("  ❌ Không lấy được dữ liệu")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
