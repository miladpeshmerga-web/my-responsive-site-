import json
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")

def load_users():
    """خوێندنەوەی لیستی بەکارهێنەران لە فایلی users.json"""
    users_list = []
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    users_list = json.load(f)
        except Exception as e:
            print(f"هەڵە لە خوێندنەوەی users.json: {e}")
    
    # دڵنیابوونەوە لەوەی ئەگەر ئایدی سەرەکی خۆت لە لیستەکەدا نەبوو، زیادی بکەین بۆ تاقیکردنەوە
    admin_id = 6782298541
    if admin_id not in users_list:
        users_list.append(admin_id)
        
    return users_list

def save_users(users):
    """پاشەکەوتکردنەوەی لیستی بەکارهێنەران بۆ ناو فایلی users.json"""
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

def send_message(chat_id, text):
    """ناردنی نامە بۆ بەکارهێنەرێکی دیاریکراو"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url, json=payload)
    print(f"وەڵامی ناردنی نامە بۆ {chat_id}: {response.json()}")
    return response.json()

def get_updates():
    """وەرگرتنی نامە نوێیەکان لە تەلەگرامەوە"""
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    response = requests.get(url)
    return response.json()

def main():
    if not TOKEN:
        print("تۆکەنی بۆت بونی نییە!")
        return

    # ۱. هێنانی لیستی بەکارهێنەران (کە ئایدی خۆت تێیدا مسۆگەرە)
    users = load_users()
    print(f"لیستی بەکارهێنەران بۆ ناردن: {users}")

    # ۲. پشکنینی نامە نوێیەکان بۆ دۆزینەوەی کەسانی تریش ئەگەر /startیان کردبێت
    updates = get_updates()
    print(f"وەڵامی getUpdates: {updates}")

    new_user_found = False
    if "result" in updates:
        for update in updates["result"]:
            if "message" in update and "chat" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")

                if text == "/start":
                    if chat_id not in users:
                        users.append(chat_id)
                        new_user_found = True
                        print(f"بەکارهێنەری نوێ دۆزرایەوە و زیادکرا: {chat_id}")

    # ٣. پاشەکەوتکردنی لیستی نوێ لە users.json
    save_users(users)

    # ٤. ناردنی نامە بۆ *هەموو* بەکارهێنەرانی ناو لیستەکە
    announcement_text = "سڵاو! ئەمە پەیامێکی تاقیکارییە لە GitHub Actionsـەوە بۆ تاقیکردنەوەی ناردنی نامە بۆ بەکارهێنەران."
    
    for user_id in users:
        send_message(user_id, announcement_text)

if __name__ == "__main__":
    main()
