from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes
from user_profile.profile_manager import get_user_settings, update_user_setting

def build_settings_menu(settings):
    buttons = [
        [InlineKeyboardButton(f"📬 Daily Digest: {'ON ✅' if settings['daily_digest'] else 'OFF ❌'}", callback_data="toggle_digest")],
        [InlineKeyboardButton(f"🎯 Alert Threshold: {settings['alert_threshold']}% (Tap to edit)", callback_data="edit_threshold")],
        [InlineKeyboardButton(f"🔕 Silent Mode: {'ON 🔇' if settings['silent_mode'] else 'OFF 🔔'}", callback_data="toggle_silent")]
    ]
    return InlineKeyboardMarkup(buttons)

async def handle_settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    settings = get_user_settings(user_id)
    reply_markup = build_settings_menu(settings)
    await update.message.reply_text("⚙️ Your Settings:", reply_markup=reply_markup) 