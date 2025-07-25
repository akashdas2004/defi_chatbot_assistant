import os
import asyncio
import time
import threading
import requests
from flask import Flask
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from alerts.alert_manager import check_alerts
from bot_core.telegram_adapter import register_handlers

load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
SELF_URL = os.environ.get(" SELF_AWAKE_URL")  # Set this on Render

# 👇 Flask server to keep Render alive
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "🤖 Bot is alive"

def run_http_server():
    flask_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# 🆕 Self-wake function that pings the server every 5 mins
def self_wake():
    while True:
        try:
            print(f"[Self-Wake] Pinging {SELF_URL}")
            requests.get(SELF_URL)
        except Exception as e:
            print(f"[Self-Wake] Failed to ping: {e}")
        time.sleep(300)  # 5 minutes

# 🧵 Start background threads
threading.Thread(target=run_http_server, daemon=True).start()
threading.Thread(target=self_wake, daemon=True).start()

# ✅ Main bot setup
async def main():
    print("🤖 Bot running...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    # Scheduler for periodic async jobs
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_alerts, trigger="interval", minutes=5)
    scheduler.start()

    await app.run_polling()

# 🔁 Entry point
if __name__ == "__main__":
    asyncio.run(main())
