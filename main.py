import os
from telegram.ext import ApplicationBuilder
from bot_core.telegram_adapter import register_handlers
from apscheduler.schedulers.background import BackgroundScheduler
from alerts.alert_manager import check_alerts
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
register_handlers(app)

scheduler = BackgroundScheduler()
scheduler.add_job(check_alerts, trigger="interval", minutes=5)
scheduler.start()

if __name__ == "__main__":
    print("🤖 Bot running...")
    app.run_polling() 