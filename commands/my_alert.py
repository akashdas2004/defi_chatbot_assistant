from user_profile.profile_manager import get_alert_threshold

def handle_my_alert(user_id):
    apy = get_alert_threshold(user_id)
    return f"📊 Your current alert is: {apy}% APY" if apy else "ℹ️ You don't have any alerts set." 