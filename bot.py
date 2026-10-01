import json
import os
import requests

# وەرگرتنی تۆکەنی بۆت لە محیطی (Environment Variables)
TOKEN = os.environ.get("BOT_TOKEN")

def get_updates(offset=None):
    """بۆ وەرگرتنی نامەکان و فەرمانەکانی بەکارهێنەران لە تەلەگرام"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    params = {"timeout": 30, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def load_users():
    """خوێندنەوەی لیستی بەکارهێنەران لە فایلی users.json"""
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_users(users):
    """پاشەکەوتکردنەوەی لیستی بەکارهێنەران بۆ ناو فایلی users.json"""
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4)

def send_message(chat_id, text):
    """ناردنی نامە بۆ بەکارهێنەرێکی دیاریکراو"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)

def main():
    if not TOKEN:
        print("تۆکەنی بۆت بونی نییە!")
        return

    # لیستی بەکارهێنەرانی پێشوو دەهێنین
    users = load_users()
    
    # پشکنینی نامە نوێیەکان (Updates) بۆ دۆزینەوەی بەکارهێنەری نوێ یان فەرمانی /start
    # تێبینی: لە کاتی کارکردنی لەسەر GitHub Actions، دەتوانین داتاکە لە getUpdates وەرگرین
    updates = get_updates()
    
    if "result" in updates:
        for update in updates["result"]:
            if "message" in update:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")
                
                # ئەگەر بەکارهێنەر فەرمانی /startی نارد، ئایدییەکەی پاشەکەوت دەکەین ئەگەر پێشتر نەبووبێت
                if text == "/start":
                    if chat_id not in users:
                        users.append(chat_id)
                        save_users(users)
                        print(f"بەکارهێنەری نوێ زیادکرا: {chat_id}")
                        send_message(chat_id, "سوپاس بۆ بەکارهێنانی بۆتەکە! تۆ بە سەرکەوتوویی تۆمار کرایت.")

    # ناردنی نامە بۆ *هەموු* ئەو بەکارهێنەرانەی کە لە لیستی users.json داتایان هەیە
    # (بۆ نموونە کاتێک دەتەوێت ئاگادارییەکی گشتی بنێریت)
    announcement_text = "سڵاو! ئەمە نامەیەکی نوێیە بۆ هەموو بەکارهێنەرانی تۆمارکراو."
    
    for user_id in users:
        send_message(user_id, announcement_text)
        print(f"نامە نێردرا بۆ: {user_id}")

if __name__ == "__main__":
    main()
