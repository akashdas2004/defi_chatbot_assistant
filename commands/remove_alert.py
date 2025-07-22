from user_profile.profile_manager import remove_alert

def handle_remove_alert(user_id):
    remove_alert(user_id)
    return "✅ Your alert has been removed." 