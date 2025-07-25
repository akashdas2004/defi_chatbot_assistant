import os
import threading
import asyncio
from flask import Flask
from telegram.ext import ApplicationBuilder
from bot_core.telegram_adapter import register_handlers
from apscheduler.schedulers.background import BackgroundScheduler
from alerts.alert_manager import check_alerts
from dotenv import load_dotenv

load_dotenv()

# Load bot token
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Start Telegram bot
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
register_handlers(app)

# ✅ Async-safe wrapper to run check_alerts
def run_check_alerts():
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(check_alerts())  # schedule coroutine
    except RuntimeError:
        asyncio.run(check_alerts())  # fallback if no running loop

# Start alert checker scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(run_check_alerts, trigger="interval", minutes=5)
scheduler.start()

# ✅ Dummy Flask server to keep Render Web Service alive
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "✅ Bot is alive."

def run_http_server():
    port = int(os.environ.get("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port)

# Start Flask server in a thread
threading.Thread(target=run_http_server, daemon=True).start()

if __name__ == "__main__":
    print("🤖 Bot running...")
    app.run_polling()
