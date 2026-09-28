import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8918413203:AAG-EBiQakMDS0jK1H3d26ox0UpBh6LN-eY"
BASE_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # دروستکردنی کلیلێکی دروستکراوی هەڕەمەکی بۆ ئەوەی ناوی کەسەکە دیار نەبێت
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
    # لینکی تایبەت کە زانیارییەکان تەنها بۆ ئەم ئایدیا دەنێرێتەوە
    unique_link = f"{BASE_URL}?ref={random_str}&id={user_id}"

    keyboard = [
        [InlineKeyboardButton("کۆپیکردنی لینکە تایبەتەکەت 🔗", callback_data="copy")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "بەخێربێیت!\n\n"
        "🔗 **لینکی تایبەتی تۆ ئامادەیە:**\n"
        f"`{unique_link}`\n\n"
        "ئەم لینکە بنێرە بۆ هەر کەسێک. کاتێک کەسەکە کلیکی لەسەر دەکات:\n"
        "1. بۆ ئەو تەنها پەیامی 'ماڵپەڕەکە لەژێر کارکردندایە' نیشان دەدرێت.\n"
        "2. بە بێ ئەوەی هەستی پێ بكات، تەواوی زانیارییەکانی مۆبایلەکەی (جۆر، شاشە، GPU) ڕاستەوخۆ لێرە بۆ تۆ دەپێسرێت!"
    )

    await update.message.reply_text(text, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("بۆتەکە چالاک بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
