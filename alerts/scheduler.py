from apscheduler.schedulers.background import BackgroundScheduler
from alerts.daily_digest import build_digest
from alerts.notification_dispatcher import send_telegram_message
from user_profile.profile_manager import load_digest_users

def start_scheduler(bot):
    scheduler = BackgroundScheduler()

    def send_daily_update():
        msg = build_digest()
        for user_id in load_digest_users():
            send_telegram_message(bot, user_id, msg, parse_mode="Markdown")

    scheduler.add_job(send_daily_update, trigger="cron", hour=9, minute=0)  # Daily at 9:00 AM
    scheduler.start() 