from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ================= CONFIG =================
TOKEN = "PASTE_NEW_BOT_TOKEN_HERE"   # <-- yahan apna NEW bot token paste karo
BOT_USERNAME = "Shein1kcouponbot"   # without @
ADMIN_ID = 7397475374
# =========================================

# In-memory storage
users = {}     # {user_id: {"points": int}}
coupons = {}   # {points: [coupon_objects]}


def is_admin(user_id: int) -> bool:
    return user_id == ADMIN_ID


# ---------------- USER COMMANDS ----------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

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
        "/refer - Get referral link\n"
        "/points - Check points\n"
        "/redeem - Redeem coupon"
    )


async def refer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    link = f"https://t.me/{BOT_USERNAME}?start={uid}"

    await update.message.reply_text(
        f"🔗 Your referral link:\n{link}\n\n"
        "Invite friends & earn 10 points per referral!"
    )


async def points(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    pts = users.get(uid, {}).get("points", 0)
    await update.message.reply_text(f"⭐ Your points: {pts}")


async def redeem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = users.get(uid)

    if not user:
        await update.message.reply_text("❌ Please use /start first")
        return

    for cost in sorted(coupons.keys()):
        if user["points"] >= cost and coupons[cost]:
            c = coupons[cost].pop(0)
            user["points"] -= cost

            msg = (
                "🎉 *Great News!* Your voucher has been assigned 🎉\n\n"
                f"*{c['title']}*\n\n"
                f"🔑 *Code:* `{c['code']}`\n\n"
                f"💰 *Amount:* {c['amount']}\n"
                f"📦 *Type:* {c['type']}\n"
                f"🛒 *Minimum Purchase:* {c['min_purchase']}\n"
                f"⏰ *Expiry Date:* {c['expiry']}\n"
                f"👤 *Assigned By:* {c['assigned_by']}"
            )

            await update.message.reply_text(msg, parse_mode="Markdown")
            return

    await update.message.reply_text("❌ Not enough points or no coupon available")


# ---------------- ADMIN COMMANDS ----------------

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("❌ Admin only")
        return

    await update.message.reply_text(
        "🛠 ADMIN PANEL\n\n"
        "/stats\n"
        "/addpoints user_id points\n"
        "/addcoupon points=50 title=Voucher#1 code=XXXX amount=1000 "
        "type=Resin min=0 expiry=31-12-2026 by=Admin\n"
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
        data = {}
        for arg in context.args:
            key, value = arg.split("=")
            data[key] = value

        points = int(data["points"])

        coupon = {
            "title": data["title"],
            "code": data["code"],
            "amount": data["amount"],
            "type": data["type"],
            "min_purchase": data["min"],
            "expiry": data["expiry"],
            "assigned_by": data["by"]
        }

        coupons.setdefault(points, []).append(coupon)

        await update.message.reply_text(
            "✅ Coupon added successfully with full details"
        )

    except:
        await update.message.reply_text(
            "❌ Wrong format!\n\n"
            "Correct:\n"
            "/addcoupon points=50 title=Voucher#1 code=XXXX amount=1000 "
            "type=Resin min=0 expiry=31-12-2026 by=Admin"
        )


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    if not context.args:
        await update.message.reply_text(
            "❌ Usage:\n/broadcast message"
        )
        return

    msg = " ".join(context.args)
    sent = 0

    for uid in users:
        try:
            await context.bot.send_message(uid, msg)
            sent += 1
        except:
            pass

    await update.message.reply_text(f"📢 Sent to {sent} users")


# ---------------- MAIN ----------------

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # user
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("refer", refer))
    app.add_handler(CommandHandler("points", points))
    app.add_handler(CommandHandler("redeem", redeem))

    # admin
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("addpoints", addpoints))
    app.add_handler(CommandHandler("addcoupon", addcoupon))
    app.add_handler(CommandHandler("broadcast", broadcast))

    print("🤖 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
