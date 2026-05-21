import requests
import time
from telegram import Bot

BOT_TOKEN = "8403169730:AAG17EecDmSekq0it7eCnDBRNvEOjl8Kkz4"
CHAT_ID = "1314410565"
COC_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjI5MDZjN2E2LTEzMDYtNDc4MC1hODlmLTY1OWI4MGJjMjVkNyIsImlhdCI6MTc3OTMzMzE0MSwic3ViIjoiZGV2ZWxvcGVyLzMyNmE2NTEyLWVlNmUtZGFkZC02Mzc4LWRlZWFkNTQyMTVjZSIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjAuMC4wLjAiXSwidHlwZSI6ImNsaWVudCJ9XX0.Hfxf1K9q4YefT2rJyWO3QnmH8DLgtz0GcL0NC24lVBhwlzbxcFd6f6428e0A-Mo9g_mb6fcAzQo0ydxP_iab9g"

bot = Bot(token=BOT_TOKEN)

headers = {
    "Authorization": f"Bearer {COC_TOKEN}"
}

checked = {}

def get_war(clan_tag):
    tag = clan_tag.replace("#", "%23")
    url = f"https://api.clashofclans.com/v1/clans/{tag}/currentwar"

    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()
    return None

while True:
    with open("clans.txt", "r") as f:
        clans = [x.strip() for x in f.readlines() if x.strip()]

    for clan in clans:
        data = get_war(clan)

        if data and "state" in data:
            state = data["state"]

            if clan not in checked:
                checked[clan] = state

            if checked[clan] != "inWar" and state == "inWar":
                clan_name = data["clan"]["name"]
                opponent = data["opponent"]["name"]

                msg = f"""
🚨 War Matched!

🏰 Clan: {clan_name}
⚔ Opponent: {opponent}
"""

                bot.send_message(chat_id=CHAT_ID, text=msg)

            checked[clan] = state

    time.sleep(300)
