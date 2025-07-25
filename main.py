import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from alerts.alert_manager import check_alerts
from bot_core.telegram_adapter import register_handlers
from flask import Flask
import threading

# Start small Flask server to bind a port (so Render doesn't shut you down)
app_http = Flask(__name__)

@app_http.route("/")
def home():
    return "🤖 Bot is alive"

def run_http_server():
    app_http.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_http_server, daemon=True).start()

# Load env vars
load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# 🧠 Define the scheduler but don’t start it yet
scheduler = AsyncIOScheduler()
scheduler.add_job(check_alerts, trigger="interval", minutes=5)

# ✅ Async entry point
async def main():
    print("🤖 Bot running...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    scheduler.start()  # 🔄 Now the event loop is running
    await app.run_polling()

# 🚀 Launch
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
