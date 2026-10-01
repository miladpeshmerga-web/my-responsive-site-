import json
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")

def load_users():
    """خوێندنەوەی لیستی بەکارهێنەران لە فایلی users.json"""
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except Exception as e:
            print(f"هەڵە لە خوێندنەوەیusers.json: {e}")
            return []
    return []

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

    # ۱. هێنانی لیستی بەکارهێنەرانی پێشوو
    users = load_users()
    print(f"بەڕێوەچوون: لیستی کۆنی بەکارهێنەران: {users}")

    # ۲. پشکنینی نامە نوێیەکان بۆ دۆزینەوەی کەسانی نوێ کە /startیان کردووە
    updates = get_updates()
    print(f"وەڵامی getUpdates: {updates}")

    new_user_found = False
    if "result" in updates:
        for update in updates["result"]:
            if "message" in update and "chat" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")

                # ئەگەر فەرمانی /startی ناردبوو وە لە لیستەکەشدا نەبوو
                if text == "/start":
                    if chat_id not in users:
                        users.append(chat_id)
                        new_user_found = True
                        print(f"بەکارهێنەری نوێ دۆزرایەوە و زیادکرا: {chat_id}")
                        # ناردنی نامەی بەخێرهاتن بۆ کەسە نوێیەکە
                        send_message(chat_id, "بەخێربێیت! تۆ بە سەرکەوتوویی لە بۆتەکەدا تۆمار کرایت.")

    # ٣. ئەگەر بەکارهێنەری نوێ زیاد بوو، فایلی users.json نوێ دەکەینەوە
    if new_user_found:
        save_users(users)
        print("فایلی users.json نوێکرایەوە.")
    else:
        print("هیچ بەکارهێنەرێکی نوێ نەدۆزرایەوە بۆ زیادکردن.")

    # ٤. (ئارەزوومەندانە): ناردنی نامەی گشتی بۆ هەموو بەکارهێنەرانی تۆمارکراو
    # ئەگەر نەتەوێت هەموو جارێک نامەی گشتی بنێررێت، دەتوانیت ئەم بەشە لابەریت
    announcement_text = "سڵاو! ئەمە پەیامێکی گشتییە لەلایەن بۆتەکەوە."
    for user_id in users:
        send_message(user_id, announcement_text)
        print(f"نامە نێردرا بۆ ئایدی: {user_id}")

if __name__ == "__main__":
    main()
