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

# 👇 Run a minimal Flask server to bind a port (keeps Render happy)
app_http = Flask(__name__)

@app_http.route("/")
def home():
    return "🤖 Bot is alive"

def run_http_server():
    app_http.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_http_server, daemon=True).start()

# ✅ Main async function for bot and scheduler
async def run_bot():
    print("🤖 Bot running...")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    register_handlers(app)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_alerts, trigger="interval", minutes=5)
    scheduler.start()

    # ✅ Don't create new event loop — just await
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# ✅ Launch the bot without crashing the event loop
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(run_bot())
        loop.run_forever()
    except KeyboardInterrupt:
        print("Bot stopped.")
