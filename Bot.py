from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

BOT_TOKEN = "8597248235:AAEf3NmHUhV-MyRO_yMJwqxp96K1GhLxv0M"
ADMIN_ID = 7397475374
BOT_ACTIVE = True
COUPON_TEXT = "🎁 SHEIN ₹1000 Coupon\n\nRefer friends and earn points!"
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    update.message.reply_text(
        f"Hi {user.first_name} 👋\n\nWelcome to SHEIN Coupon Bot 🎉\n\nUse /help to see commands."
    )

def help_cmd(update: Update, context: CallbackContext):
    update.message.reply_text(
        "/start - Start bot\n"
        "/help - Show help\n"
        "/coupon - Get coupon info"
    )

def coupon(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎁 SHEIN ₹1000 Coupon\n\n"
        "Refer friends and earn points!\n"
        "More features coming soon 🔥"
    )

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_cmd))
    dp.add_handler(CommandHandler("coupon", coupon))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
