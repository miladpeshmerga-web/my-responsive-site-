import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

# توکنی فەرمی بۆتەکەت
TOKEN = "8918413203:AAG-EBiQakMDS0jK1H3d26ox0UpBh6LN-eY"

# لینکی ماڵپەڕە ڕیسپۆنسیڤەکەت
WEBSITE_URL = "https://miladpeshmerga-web.github.io/my-responsive-site-/"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("کردنەوە لە وێبگەڕ 🌐", url=WEBSITE_URL)],
        [InlineKeyboardButton("کردنەوە لەناو تێلێگرام 📱", web_app=WebAppInfo(url=WEBSITE_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "بەخێربێیت! بۆ دیدەنی ماڵپەڕەکە کلیک لەسەر یەکێک لە دوگمەکانی خوارەوە بکە:",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    print("بۆتەکە چالاک بوو...")
    app.run_polling()

if __name__ == "__main__":
    main()
