from user_profile.profile_manager import save_alert_threshold

def handle_set_alert(user_id: int, apy_threshold: float):
    save_alert_threshold(user_id, apy_threshold)
    return f"🔔 Alert set! You'll be notified if APY goes above {apy_threshold}%." 