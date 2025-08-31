import telebot
from telebot import types

# === CONFIG ===
TOKEN = "YOUR_BOT_TOKEN"  # BotFather se mila token
target_channel = "@your_channel"  # jaha logs save karne hain
OWNER_ID = 123456789  # apna Telegram ID yaha dalna

bot = telebot.TeleBot(TOKEN)

# === DATA STORAGE ===
admins = [OWNER_ID]  # by default owner hi admin hoga
trade_id = 1  # starting Trade ID

# === HELP FUNCTION ===
def is_admin(user_id):
    return user_id in admins or user_id == OWNER_ID

# === COMMANDS ===
@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "👋 Welcome to Escrow Bot! Use /add, /done, /refund commands (Admins only).")

# === ADD ADMIN ===
@bot.message_handler(commands=["addAdmin"])
def add_admin(msg):
    if msg.from_user.id != OWNER_ID:
        bot.reply_to(msg, "⛔ Permission Denied! Sirf Owner Admin add kar sakta hai.")
        return
    try:
        username = msg.text.split()[1]
        if username.startswith("@"): username = username[1:]
        user_id = username  # Normally yaha user_id fetch karna hoga
        # For simplicity hum username store kar rahe hain
        admins.append(username)
        bot.reply_to(msg, f"✅ @{username} ab Escrow Admin ban gaya hai.")
    except:
        bot.reply_to(msg, "❌ Usage: /addAdmin @username")

# === REMOVE ADMIN ===
@bot.message_handler(commands=["removeAdmin"])
def remove_admin(msg):
    if msg.from_user.id != OWNER_ID:
        bot.reply_to(msg, "⛔ Permission Denied! Sirf Owner Admin hata sakta hai.")
        return
    try:
        username = msg.text.split()[1]
        if username.startswith("@"): username = username[1:]
        if username in admins:
            admins.remove(username)
            bot.reply_to(msg, f"❌ @{username} ab Admin nahi raha.")
        else:
            bot.reply_to(msg, "⚠️ Ye user Admin list me nahi hai.")
    except:
        bot.reply_to(msg, "❌ Usage: /removeAdmin @username")

# === ADD DEAL ===
@bot.message_handler(commands=["add", "add+fee"])
def add_deal(msg):
    global trade_id
    if not is_admin(msg.from_user.id):
        bot.reply_to(msg, "⛔ Sirf Admin Deal Add kar sakta hai.")
        return

    parts = msg.text.split(" ")
    if len(parts) < 4:
        bot.reply_to(msg, "❌ Usage: /add buyer seller amount")
        return

    buyer, seller, amount = parts[1], parts[2], parts[3]
    fee = "3%" if msg.text.startswith("/add+fee") else "0"

    text = f"""✅ PAYMENT RECEIVED
────────────────
👤 Buyer  : {buyer}
👤 Seller : {seller}
💸 Received : ₹{amount}
🆔 Trade ID : #TID{trade_id}
💰 Fee     : {fee}
CONTINUE DEAL ❤️
────────────────"""

    bot.send_message(msg.chat.id, text)
    trade_id += 1

# === DONE DEAL ===
@bot.message_handler(commands=["done", "done+fee"])
def done_deal(msg):
    if not is_admin(msg.from_user.id):
        bot.reply_to(msg, "⛔ Sirf Admin Deal Complete kar sakta hai.")
        return

    parts = msg.text.split(" ")
    if len(parts) < 4:
        bot.reply_to(msg, "❌ Usage: /done buyer seller amount")
        return

    buyer, seller, amount = parts[1], parts[2], parts[3]
    fee = "3%" if msg.text.startswith("/done+fee") else "0"

    text = f"""✅ DEAL COMPLETED
────────────────
👤 Buyer  : {buyer}
👤 Seller : {seller}
💰 Amount : ₹{amount}
🆔 Trade ID : Auto
💰 Fee     : {fee}
────────────────
🛡️ Escrowed by @{msg.from_user.username}"""

    bot.send_message(msg.chat.id, text)
    bot.send_message(target_channel, text.replace("✅ DEAL COMPLETED", "📜 Deal Completed (Log)"))

# === REFUND DEAL ===
@bot.message_handler(commands=["refund", "refund+fee"])
def refund_deal(msg):
    if not is_admin(msg.from_user.id):
        bot.reply_to(msg, "⛔ Sirf Admin Refund kar sakta hai.")
        return

    parts = msg.text.split(" ")
    if len(parts) < 4:
        bot.reply_to(msg, "❌ Usage: /refund buyer seller amount")
        return

    buyer, seller, amount = parts[1], parts[2], parts[3]
    fee = "3%" if msg.text.startswith("/refund+fee") else "0"

    text = f"""❌ REFUND COMPLETED
────────────────
👤 Buyer  : {buyer}
👤 Seller : {seller}
💰 Refund : ₹{amount}
🆔 Trade ID : Auto
💰 Fee     : {fee}
────────────────
🛡️ Escrowed by @{msg.from_user.username}"""

    bot.send_message(msg.chat.id, text)
    bot.send_message(target_channel, text.replace("❌ REFUND COMPLETED", "📜 Refund Log"))

# === RUN BOT ===
bot.infinity_polling()
