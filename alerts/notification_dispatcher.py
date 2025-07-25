from telegram import Bot
import os

bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])

def send_alert(user_id, message):
    bot.send_message(chat_id=user_id, text=message)

def send_telegram_message(bot, user_id, text, parse_mode=None):
    try:
        bot.send_message(chat_id=user_id, text=text, parse_mode=parse_mode)
    except Exception as e:
        print(f"❌ Failed to send message to {user_id}: {e}") 