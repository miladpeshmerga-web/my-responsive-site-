import os
import sys
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8918413203:AAG-EBiQakMDS0jK1H3d26ox0UpBh6LN-eY"
BASE_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"
CHAT_ID = "6782298541" # چات ئایدی خۆت بۆ کاتی کارکردنی ڕاستەوخۆ لە GitHub Actions

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    link = f"{BASE_URL}?id={user_id}"

    text = (
        "بەخێربێیت!\n\n"
        "🔗 **لینکی تایبەتی تۆ ئامادەیە:**\n"
        f"{link}\n\n"
        "تکایە کلیک لەسەر لینکەکە بکە."
    )

    await update.message.reply_text(text, disable_web_page_preview=True, parse_mode='Markdown')

def send_direct_link():
    link = f"{BASE_URL}?id={CHAT_ID}"
    text = (
        "بەخێربێیت! (نێردرا لەڕێگەی GitHub Actionsـەوە)\n\n"
        "🔗 **لینکی تایبەتی تۆ ئامادەیە:**\n"
        f"{link}\n\n"
        "تکایە کلیک لەسەر لینکەکە بکە."
    )
    
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("لینک بە سەرکەوتوویی لە GitHub Actionsـەوە نێردرا بۆ تێلێگرام!")
    else:
        print("هەڵە لە ناردنی نامە:", response.text)

def main():
    # ئەگەر لە GitHub Actions بوو، تەنها یەکجار لینکەکە بنێرە و کۆتایی بهێنە
    if os.getenv("GITHUB_ACTIONS") == "true":
        print("سیستەم لەسەر GitHub Actions کار دەکات، ناردنی ڕاستەوخۆی لینک...")
        send_direct_link()
        return

    # بۆ کاتی کارکردنی ئاسایی (Polling) بۆ ئەوەی فەرمانی /start هەمیشە کاربکات
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("بۆتەکە بە شێوەی پۆلینگ چالاک بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
