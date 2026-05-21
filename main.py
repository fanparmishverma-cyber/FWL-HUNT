from telegram.ext import Updater, CommandHandler

TOKEN = "8602830344:AAHgvaxoEc4uU5NoWEAHFYh71JenJHJZejo"

def start(update, context):
    update.message.reply_text("✅ Bot is working!")

def ping(update, context):
    update.message.reply_text("🏓 Pong!")

updater = Updater(TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("ping", ping))

updater.start_polling()
updater.idle()
