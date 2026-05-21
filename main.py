import requests
import time
import threading
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode

BOT_TOKEN = "8602830344:AAHgvaxoEc4uU5NoWEAHFYh71JenJHJZejo"
CHAT_ID = "1314410565"
COC_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjI5MDZjN2E2LTEzMDYtNDc4MC1hODlmLTY1OWI4MGJjMjVkNyIsImlhdCI6MTc3OTMzMzE0MSwic3ViIjoiZGV2ZWxvcGVyLzMyNmE2NTEyLWVlNmUtZGFkZC02Mzc4LWRlZWFkNTQyMTVjZSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjAuMC4wLjAiXSwidHlwZSI6ImNsaWVudCJ9XX0.Hfxf1K9q4YefT2rJyWO3QnmH8DLgtz0GcL0NC24lVBhwlzbxcFd6f6428e0A-Mo9g_mb6fcAzQo0ydxP_iab9g"

headers = {
    "Authorization": f"Bearer {COC_TOKEN}"
}

updater = Updater(BOT_TOKEN, use_context=True)
bot = updater.bot

tracked_clans = [
    "#9288QU9U",
    "#2L8YVG9LU",
    "#2GQYV2VJJ",
    "#LYGY8UQ",
    "#8GY98CV",
    "#QCQR2PCP",
    "#JUCGUPYC",
    "#22GQYPLQ",
    "#2LCRG22UY",
    "#2808CJPQ9",
    "#GPUCC2PY",
    "#PQC00PC9",
    "#2PLJJ9LJR",
    "#2RCVU8U88",
    "#U82UC00Y",
    "#2QVC9VGPP",
    "#RC2R8YYC",
    "#28G2P9J8G",
    "#LCUQPJ00",
    "#2GR9RCV0Y",
    "#Y00V9QYL",
    "#G288GLU8",
    "#289GJL0LV",
    "#UCCYY89J",
    "#RGQR2RQ0",
    "#YPY2GYJJ",
    "#R9YLPJ9",
    "#U2LG292G",
    "#YQR2QLY",
    "#CQ9YUPQ0",
    "#YV2CLC9Y",
    "#VGCGR8UR",
    "#9V88GUR2",
    "#VPJC98R0",
    "#2PPUL9QCV",
    "#29Q0J9JGP",
    "#892UVQ99",
    "#LUY9RV0G",
    "#28U8G9L9Q",
    "#9908YV8R",
    "#PY2QU8QL",
    "#9LPR8QLP",
    "#2L28RG9QP",
    "#9GL0L00J",
    "#2J2R9YRY8",
    "#P9VC20RJ",
    "#GRRG8CJQ",
    "#VCQ9QQR",
    "#QGVCLYGG",
    "#V208G0GU",
    "#G2029J22",
    "#89LURCCL",
    "#JQ829JVJ",
    "#9U82V0J0",
    "#2YL0JP9GU",
    "#28YUL0QVY",
    "#2L0VYQRQL",
    "#2CC8JG8P8",
    "#2RVPCJYC",
    "#RC2C20CU",
    "#LQCULV9",
    "#22GGGGVYR",
    "#LL8UCRGL",
    "#98V2RP9R",
    "#RG0C8Q9L",
    "#8GC8PQPR",
    "#R89LQY9V",
    "#280LLG0UV",
    "#2PLQYQYGC",
    "#2Q0PR82L9",
    "#YUY92U2R",
    "#VYURPVRY",
    "#P29CJUP8",
    "#29V9YQ9Y9",
    "#YUUUVR8P",
    "#2RGY0QYY0",
    "#PJY2C2CR",
    "#JJLPP2QR",
    "#Y2G9Q8VV",
    "#P2J"
]
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
        "/clans\n"
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



def clans(update, context):
    if not tracked_clans:
        update.message.reply_text("No clans added")
        return

    msg = "🏰 Tracked Clans:\n\n"

    for clan in tracked_clans:
        msg += f"{clan}\n"

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
                        text=msg,
                        parse_mode=ParseMode.HTML
                    )

                checked[clan] = state

        time.sleep(300)


# =========================
# HANDLERS
# =========================


dp = updater.dispatcher


dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("ping", ping))
dp.add_handler(CommandHandler("addclan", addclan))
dp.add_handler(CommandHandler("removeclan", removeclan))
dp.add_handler(CommandHandler("clans", clans))
dp.add_handler(CommandHandler("adduser", adduser))
dp.add_handler(CommandHandler("users", users))
dp.add_handler(CommandHandler("track", track))
dp.add_handler(CommandHandler("stop", stop))


threading.Thread(target=war_loop).start()

updater.start_polling()
updater.idle()
