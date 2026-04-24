import requests
import os
from datetime import datetime

BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', "8727925469:AAGDq2pNNekunJInbLVi9akdcri7zav-sfY")
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', 8114628397)
BALANCE_FILE = "last_balance.txt"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
        return True
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
        response = requests.post(url, headers=headers, json={}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "0":
                user_data = data["data"]
                nickname = user_data.get("nickName", "N/A")
                income = int(float(user_data.get("income", 0)))
                return nickname, income
    except:
        pass
    return None, None

def format_money(amount):
    return f"{amount:,} VND".replace(",", ".")

def read_last_balance():
    try:
        with open(BALANCE_FILE, 'r') as f:
            return int(f.read().strip())
    except:
        return None

def save_last_balance(balance):
    with open(BALANCE_FILE, 'w') as f:
        f.write(str(balance))

def main():
    print(f"[{datetime.now()}] Kiểm tra...")
    nickname, current_balance = get_user_data()
    
    if current_balance is not None:
        print(f"👤 {nickname} | 💰 {format_money(current_balance)}")
        last_balance = read_last_balance()
        save_last_balance(current_balance)
        
        if last_balance is not None and current_balance != last_balance:
            change = current_balance - last_balance
            change_symbol = "+" if change > 0 else ""
            message = f"👤 @{nickname}\n💰 {format_money(current_balance)}\n🔄 {change_symbol}{format_money(abs(change))}"
            send_telegram_message(message)
            print(f"✅ Đã gửi: {change_symbol}{format_money(abs(change))}")
        else:
            print("✅ Không đổi")
    else:
        print("❌ Lỗi")

if __name__ == "__main__":
    main()
