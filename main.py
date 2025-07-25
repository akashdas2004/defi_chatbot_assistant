import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot_core.telegram_adapter import register_handlers
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # ✅ Async scheduler
from alerts.alert_manager import check_alerts

# Optional: Self-ping HTTP server to keep Render port open
from flask import Flask
import threading

app_http = Flask(__name__)

@app_http.route("/")
def home():
    return "🤖 Bot is alive"

def run_http_server():
    app_http.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

threading.Thread(target=run_http_server, daemon=True).start()

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

# Build Telegram bot app
app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
register_handlers(app)

# ✅ Use AsyncIOScheduler to support async check_alerts
scheduler = AsyncIOScheduler()
scheduler.add_job(check_alerts, trigger="interval", minutes=5)
scheduler.start()

if __name__ == "__main__":
    print("🤖 Bot running...")
    app.run_polling()
