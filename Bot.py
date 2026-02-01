users = {}
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")
BOT_USERNAME = "Shein1kCouponBot"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = user.id

    if user_id not in users:
        users[user_id] = {
            "points": 0,
            "referred_by": None
        }

        # referral detect
        if context.args:
            referrer_id = int(context.args[0])
            if referrer_id != user_id and referrer_id in users:
                users[user_id]["referred_by"] = referrer_id
                users[referrer_id]["points"] += 10  # referral reward

    await update.message.reply_text(
        "👋 Welcome to SHEIN Coupon Bot 🎉\n\n"
        "🎁 Refer friends & earn points\n"
        "📌 Use /points to check points\n"
        "🎁 Use /redeem to redeem"
    )
    async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    points = users.get(user_id, {}).get("points", 0)

    await update.message.reply_text(
        f"⭐ Your current points: {points}"
    )
    async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.get(user_id)

    if not user or user["points"] < 50:
        await update.message.reply_text(
            "❌ Not enough points.\n\nYou need at least 50 points to redeem."
        )
        return

    user["points"] -= 50

    await update.message.reply_text(
        "🎉 Redemption successful!\n\n"
        "₹100 SHEIN coupon unlocked 🎁"
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

def main(app.add_handler(CommandHandler("points", points))
app.add_handler(CommandHandler("redeem", redeem))):
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("refer", refer))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
