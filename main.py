import requests
import time
import threading
from telegram.ext import Updater, CommandHandler

BOT_TOKEN = "8602830344:AAHgvaxoEc4uU5NoWEAHFYh71JenJHJZejo"
CHAT_ID = "1314410565"
COC_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjI5MDZjN2E2LTEzMDYtNDc4MC1hODlmLTY1OWI4MGJjMjVkNyIsImlhdCI6MTc3OTMzMzE0MSwic3ViIjoiZGV2ZWxvcGVyLzMyNmE2NTEyLWVlNmUtZGFkZC02Mzc4LWRlZWFkNTQyMTVjZSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjAuMC4wLjAiXSwidHlwZSI6ImNsaWVudCJ9XX0.Hfxf1K9q4YefT2rJyWO3QnmH8DLgtz0GcL0NC24lVBhwlzbxcFd6f6428e0A-Mo9g_mb6fcAzQo0ydxP_iab9g"

headers = {
    "Authorization": f"Bearer {COC_TOKEN}"
}

updater = Updater(BOT_TOKEN, use_context=True)
bot = updater.bot

tracked_clans = []
mentioned_users = []
checked = {}
tracking = False

# =========================
# COMMANDS
# =========================

def start(update, context):
    update.message.reply_text(
        "✅ Clash Tracker Bot Online\n\n"
        "/addclan #TAG\n"
        "/removeclan #TAG\n"
        "/searchclan #TAG\n"
        "/clans\n"
        "/notinwar\n"
        "/adduser @username\n"
        "/users\n"
        "/track\n"
        "/stop\n"
        "/ping"
    )

def ping(update, context):
    update.message.reply_text("🏓 Pong! Bot is working.")

def addclan(update, context):

    global tracked_clans

    if len(context.args) == 0:
        update.message.reply_text("Usage: /addclan #TAG")
        return

    clan = context.args[0].upper()

    if clan not in tracked_clans:
        tracked_clans.append(clan)
        update.message.reply_text(f"✅ Added clan {clan}")
    else:
        update.message.reply_text("Clan already added")

def removeclan(update, context):

    global tracked_clans

    if len(context.args) == 0:
        update.message.reply_text("Usage: /removeclan #TAG")
        return

    clan = context.args[0].upper()

    if clan in tracked_clans:
        tracked_clans.remove(clan)
        update.message.reply_text(f"❌ Removed clan {clan}")
    else:
        update.message.reply_text("Clan not found")

def searchclan(update, context):

    if len(context.args) == 0:
        update.message.reply_text("Usage: /searchclan #TAG")
        return

    clan = context.args[0].upper()

    if clan in tracked_clans:
        update.message.reply_text(f"✅ {clan} is being tracked")
    else:
        update.message.reply_text(f"❌ {clan} not found")

def clans(update, context):

    if not tracked_clans:
        update.message.reply_text("No clans added")
        return

    msg = f"🏰 Total Clans: {len(tracked_clans)}\n\n"

    for i, clan in enumerate(tracked_clans, start=1):
        msg += f"{i}. {clan}\n"

    update.message.reply_text(msg)

def notinwar(update, context):

    msg = "❌ Clans Not In War:\n\n"

    count = 0

    for clan in tracked_clans:

        data = get_war(clan)

        if not data:
            continue

        state = data.get("state", "")

        if state != "inWar" and state != "preparation":

            msg += f"{clan}\n"
            count += 1

    if count == 0:
        msg = "✅ All clans are in war/preparation"

    update.message.reply_text(msg)

def adduser(update, context):

    global mentioned_users

    if len(context.args) == 0:
        update.message.reply_text("Usage: /adduser @username")
        return

    user = context.args[0]

    if user not in mentioned_users:
        mentioned_users.append(user)
        update.message.reply_text(f"✅ Added {user}")
    else:
        update.message.reply_text("User already added")

def users(update, context):

    if not mentioned_users:
        update.message.reply_text("No users added")
        return

    msg = "👥 Mention Users:\n\n"

    for user in mentioned_users:
        msg += f"{user}\n"

    update.message.reply_text(msg)

def track(update, context):

    global tracking

    tracking = True

    update.message.reply_text("🚀 Tracking Started")

def stop(update, context):

    global tracking

    tracking = False

    update.message.reply_text("⛔ Tracking Stopped")

# =========================
# WAR CHECKER
# =========================

def get_war(clan_tag):

    tag = clan_tag.replace("#", "%23")

    url = f"https://api.clashofclans.com/v1/clans/{tag}/currentwar"

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()

    return None

def war_loop():

    global checked

    while True:

        if tracking:

            for clan in tracked_clans:

                data = get_war(clan)

                if not data:
                    continue

                if "state" not in data:
                    continue

                state = data["state"]

                if clan not in checked:
                    checked[clan] = state

                # Detect preparation day
                if checked[clan] != "preparation" and state == "preparation":

                    clan_name = data["clan"]["name"]
                    opponent = data["opponent"]["name"]

                    mentions = " ".join(mentioned_users)

                    msg = (
                        f"🚨 WAR MATCHED 🚨\n\n"
                        f"🏰 Clan: {clan_name}\n"
                        f"⚔ Opponent: {opponent}\n\n"
                        f"{mentions}"
                    )

                    bot.send_message(
                        chat_id=CHAT_ID,
                        text=msg
                    )

                checked[clan] = state

        # CHECK EVERY 1 MINUTE
        time.sleep(60)

# =========================
# HANDLERS
# =========================

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("ping", ping))
dp.add_handler(CommandHandler("addclan", addclan))
dp.add_handler(CommandHandler("removeclan", removeclan))
dp.add_handler(CommandHandler("searchclan", searchclan))
dp.add_handler(CommandHandler("clans", clans))
dp.add_handler(CommandHandler("notinwar", notinwar))
dp.add_handler(CommandHandler("adduser", adduser))
dp.add_handler(CommandHandler("users", users))
dp.add_handler(CommandHandler("track", track))
dp.add_handler(CommandHandler("stop", stop))

threading.Thread(target=war_loop).start()

updater.start_polling()
updater.idle()
