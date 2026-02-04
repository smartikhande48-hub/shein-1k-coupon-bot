from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8456892529:AAEGU-GAR1joqmCjq9Qjr5QDIN2q3uv8Y8k"
BOT_USERNAME = "Lol_autobot"
ADMIN_ID = 8456892529

users = {}
coupons = []          # list = stock
admin_waiting_coupon = set()


def is_admin(uid):
    return uid == ADMIN_ID


# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if uid not in users:
        users[uid] = {"points": 0}

        if context.args:
            try:
                ref = int(context.args[0])
                if ref != uid and ref in users:
                    users[ref]["points"] += 10
            except:
                pass

    await update.message.reply_text(
        "👋 Welcome to SHEIN Coupon Bot\n\n"
        "/refer - Referral link\n"
        "/points - Your points\n"
        "/redeem - Redeem coupon\n"
        "/stock - Check coupon stock"
    )


# ---------------- USER COMMANDS ----------------
async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    link = f"https://t.me/{BOT_USERNAME}?start={uid}"
    await update.message.reply_text(f"🔗 Your referral link:\n{link}")


async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    await update.message.reply_text(f"⭐ Your points: {users.get(uid, {}).get('points', 0)}")


async def stock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"🎟 Available coupons: {len(coupons)}"
    )


async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if users.get(uid, {}).get("points", 0) < 50:
        await update.message.reply_text("❌ Not enough points (need 50)")
        return

    if not coupons:
        await update.message.reply_text("❌ No coupon available right now")
        return

    users[uid]["points"] -= 50
    coupon_text = coupons.pop(0)   # stock -1

    await update.message.reply_text(
        "🎉 *Great News! Your voucher has been assigned* 🎉\n\n"
        + coupon_text,
        parse_mode="Markdown"
    )


# ---------------- ADMIN PANEL ----------------
async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\n"
        "/addcoupon - Add coupon\n"
        "/addpoints user_id points\n"
        "/stats"
    )


async def addcoupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    admin_waiting_coupon.add(update.effective_user.id)
    await update.message.reply_text(
        "✍️ Ab coupon details bhejo.\n"
        "Jo likhoge wahi user ko milega.\n\n"
        "📦 Stock +1 automatically"
    )


async def receive_coupon(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id

    if uid in admin_waiting_coupon:
        coupons.append(update.message.text)   # stock +1
        admin_waiting_coupon.remove(uid)

        await update.message.reply_text(
            f"✅ Coupon added successfully\n"
            f"📦 Current stock: {len(coupons)}"
        )


async def addpoints(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    try:
        uid = int(context.args[0])
        pts = int(context.args[1])
        users.setdefault(uid, {"points": 0})
        users[uid]["points"] += pts
        await update.message.reply_text("✅ Points added")
    except:
        await update.message.reply_text("❌ /addpoints user_id points")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        f"👥 Users: {len(users)}\n"
        f"🎟 Coupons stock: {len(coupons)}"
    )


# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("redeem", redeem))
    app.add_handler(CommandHandler("stock", stock))

    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("addcoupon", addcoupon))
    app.add_handler(CommandHandler("addpoints", addpoints))
    app.add_handler(CommandHandler("stats", stats))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_coupon))

    app.run_polling()


if __name__ == "__main__":
    main()
