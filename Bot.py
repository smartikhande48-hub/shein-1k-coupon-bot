import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "Shein1kCouponBot"

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
    user_id = update.effective_user.id
    referral_link = "https://t.me/" + BOT_USERNAME + "?start=" + str(user_id)

    await update.message.reply_text(
        "🔗 Your referral link:\n\n" + referral_link
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
