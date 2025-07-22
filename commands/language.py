from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from user_profile.profile_manager import set_language, get_user_settings
from lang_manager import t

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [
        [InlineKeyboardButton("🇬🇧 English", callback_data="lang_en")],
        [InlineKeyboardButton("🇮🇳 Hindi", callback_data="lang_hi")],
        [InlineKeyboardButton("🇪🇸 Spanish", callback_data="lang_es")]
    ]
    markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("🌐 Select your language:", reply_markup=markup)

async def handle_language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[-1]
    set_language(query.from_user.id, lang)
    await query.edit_message_text("✅ Language updated.") 