from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================== CONFIG ==================
TOKEN = "8597248235:AAEf3NmHUhV-MyRO_yMJwqxp96K1GhLxv0M"
BOT_USERNAME = "Shein1kcouponbot"
ADMIN_ID = 7397475374
# ============================================

# In-memory storage
users = {}      # {user_id: {"points": int}}
coupons = {}    # {points_required: [code1, code2]}


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ------------------ USER COMMANDS ------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # register user
    if user_id not in users:
        users[user_id] = {"points": 0}

        # referral logic
        if context.args:
            try:
                ref_id = int(context.args[0])
                if ref_id != user_id and ref_id in users:
                    users[ref_id]["points"] += 10
            except:
                pass

    await update.message.reply_text(
        "👋 Welcome to SHEIN Coupon Bot 🎉\n\n"
        "Earn points via referrals & redeem coupons!\n\n"
        "Commands:\n"
        "/refer - Get referral link\n"
        "/points - Check points\n"
        "/redeem - Redeem coupon"
    )


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    await update.message.reply_text(
        f"🔗 Your referral link:\n{link}\n\n"
        "Invite friends & earn points!"
    )


async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    pts = users.get(user_id, {}).get("points", 0)
    await update.message.reply_text(f"⭐ Your points: {pts}")


async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = users.get(user_id)

    if not user:
        await update.message.reply_text("❌ Please use /start first")
        return

    for cost in sorted(coupons.keys()):
        if user["points"] >= cost and coupons[cost]:
            code = coupons[cost].pop(0)
            user["points"] -= cost

            await update.message.reply_text(
                f"🎉 Coupon Redeemed!\n\n"
                f"🎟 Code: {code}\n"
                f"⭐ Points used: {cost}"
            )
            return

    await update.message.reply_text(
        "❌ Not enough points or no coupons available"
    )


# ------------------ ADMIN COMMANDS ------------------

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only")
        return

    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\n"
        "/stats - Bot stats\n"
        "/addpoints user_id points\n"
        "/addcoupon points coupon_code\n"
        "/broadcast message"
    )


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    total_users = len(users)
    total_points = sum(u["points"] for u in users.values())

    await update.message.reply_text(
        f"📊 BOT STATS\n\n"
        f"👥 Users: {total_users}\n"
        f"⭐ Total points: {total_points}"
    )


async def addpoints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    try:
        uid = int(context.args[0])
        pts = int(context.args[1])

        users.setdefault(uid, {"points": 0})
        users[uid]["points"] += pts

        await update.message.reply_text("✅ Points added successfully")
    except:
        await update.message.reply_text(
            "❌ Usage:\n/addpoints user_id points"
        )


async def addcoupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    try:
        pts = int(context.args[0])
        code = context.args[1]

        coupons.setdefault(pts, []).append(code)

        await update.message.reply_text(
            f"✅ Coupon added\n\n"
            f"🎟 Code: {code}\n"
            f"⭐ Required points: {pts}"
        )
    except:
        await update.message.reply_text(
            "❌ Usage:\n/addcoupon points coupon_code"
        )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/broadcast message"
        )
        return

    message = " ".join(context.args)
    sent = 0

    for uid in users:
        try:
            await context.bot.send_message(uid, message)
            sent += 1
        except:
            pass

    await update.message.reply_text(
        f"📢 Broadcast sent to {sent} users"
    )


# ------------------ MAIN ------------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # user commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("redeem", redeem))

    # admin commands
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("addpoints", addpoints))
    app.add_handler(CommandHandler("addcoupon", addcoupon))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("🤖 Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
