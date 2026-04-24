import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', "8727925469:AAGDq2pNNekunJInbLVi9akdcri7zav-sfY")
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 8114628397)

BALANCE_FILE = "last_balance.txt"
STARTUP_FILE = "startup_sent.txt"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, json=payload, timeout=5)
        return r.status_code == 200
    except:
        return False

def get_user_data():
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
        resp = requests.post(url, headers=headers, json={}, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("code") == "0":
                user_data = data["data"]
                return user_data.get("nickName", "N/A"), int(float(user_data.get("income", 0)))
        return None, None
    except:
        return None, None

def format_money(amount):
    return f"{amount:,} VND".replace(",", ".")

def read_balance():
    try:
        with open(BALANCE_FILE, 'r') as f:
            return int(f.read())
    except:
        return None

def write_balance(balance):
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def already_started():
    try:
        with open(STARTUP_FILE, 'r'):
            return True
    except:
        return False

def mark_started():
    with open(STARTUP_FILE, 'w') as f:
        f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

def main():
    print("=" * 50)
    print("   THEO DÕI BIẾN ĐỘNG SỐ DƯ")
    print("=" * 50)
    
    nickname, current = get_user_data()
    if current is None:
        print("❌ Không lấy được dữ liệu")
        return
    
    print(f"👤 {nickname} | 💰 {format_money(current)}")
    
    # ---- Lần đầu chạy ----
    if not already_started():
        msg = f"🚀 BOT ĐÃ BẮT ĐẦU CHẠY 🚀\n\n👤 @{nickname}\n💰 Số dư gốc: {format_money(current)}\n⏱️ Kiểm tra mỗi 5 phút"
        if send_telegram_message(msg):
            mark_started()
            write_balance(current)  # Lưu số dư gốc
            print("✅ Đã gửi thông báo bắt đầu")
        return
    
    # ---- Kiểm tra biến động ----
    last = read_balance()
    if last is None:
        write_balance(current)
        print("📝 Đã lưu số dư hiện tại")
        return
    
    if current != last:
        change = current - last
        symbol = "+" if change > 0 else ""
        
        msg = f"👤 @{nickname}\n💰 {format_money(current)}\n🔄 {symbol}{format_money(abs(change))}"
        
        if send_telegram_message(msg):
            write_balance(current)  # ✅ QUAN TRỌNG: Cập nhật số dư mới
            print(f"⚡ Đã gửi biến động: {symbol}{format_money(abs(change))}")
        else:
            print("❌ Gửi thất bại")
    else:
        print("✅ Không có biến động")
    
    print("=" * 50)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Lỗi: {e}")
