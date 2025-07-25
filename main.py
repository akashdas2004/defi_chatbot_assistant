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
    if "RENDER" in os.environ or "RENDER_EXTERNAL_HOSTNAME" in os.environ:
        # Use webhook mode on Render
        app.run_webhook(
            listen="0.0.0.0",
            port=int(os.environ.get("PORT", 10000)),
            url_path=TELEGRAM_BOT_TOKEN,
            webhook_url=f"https://defi-chatbot-assistant.onrender.com/{TELEGRAM_BOT_TOKEN}"
        )
    else:
        app.run_polling() 