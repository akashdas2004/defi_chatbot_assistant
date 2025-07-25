import os
import asyncio
import threading
from flask import Flask
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from alerts.alert_manager import check_alerts
from bot_core.telegram_adapter import register_handlers

load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Start Flask server to keep Render port alive
app_http = Flask(__name__)

@app_http.route("/")
def home():
    return "🤖 Bot is alive"

def run_http_server():
    app_http.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# Launch Flask in background
threading.Thread(target=run_http_server, daemon=True).start()

# 🚀 Async startup
async def main():
    print("🤖 Bot running...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    # Start async scheduler only after event loop is alive
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_alerts, trigger="interval", minutes=5)
    scheduler.start()

    await app.run_polling()

# 🧠 Fix: Don't use asyncio.run() if event loop is running (Render may run one)
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # For environments where event loop is already running (Jupyter, Flask, etc.)
            loop.create_task(main())
        else:
            loop.run_until_complete(main())
    except RuntimeError:
        # In case no event loop is present
        asyncio.run(main())
