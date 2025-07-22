from user_profile.profile_manager import add_digest_user, remove_digest_user

def handle_daily_on(user_id: int) -> str:
    add_digest_user(user_id)
    return "✅ Daily digest enabled! You'll get DeFi updates every morning."

def handle_daily_off(user_id: int) -> str:
    remove_digest_user(user_id)
    return "🛑 Daily digest disabled. You can turn it on anytime with /dailyon" 