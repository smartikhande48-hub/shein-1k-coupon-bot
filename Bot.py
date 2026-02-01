import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Hi!\n\nWelcome to SHEIN Coupon Bot 🎉\n\nUse /help to see commands."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 Available Commands:\n\n"
        "/start - Start the bot\n"
        "/help - Show help\n"
        "/refer - Get referral info"
    )

async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔗 Refer friends and earn points!\n\nMore features coming soon 🔥"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("refer", refer))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
