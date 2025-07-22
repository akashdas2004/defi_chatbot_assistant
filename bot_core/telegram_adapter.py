from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler, InlineQueryHandler
from telegram.constants import ParseMode
from commands.top_vaults import get_top_vaults_text
from commands.set_alert import handle_set_alert
from commands.my_alert import handle_my_alert
from commands.remove_alert import handle_remove_alert
from commands.summary import generate_summary
from commands.market import format_market_data
from commands.explain import handle_explain
from commands.define import handle_define
from commands.daily_optin import handle_daily_on, handle_daily_off
from commands.logsummary import handle_log_summary
from analytics.usage_tracker import track_usage
from commands.start import handle_start
from commands.help import handle_help
import asyncio
import uuid
from commands.inline_search import search_inline_results
from commands.market_paginator import handle_market, handle_market_pagination
from commands.summary_paginator import handle_summary, handle_summary_pagination
from commands.settings import handle_settings, build_settings_menu
from user_profile.profile_manager import update_user_setting, get_user_settings
from telegram.ext import MessageHandler, filters
from commands.language import handle_language, handle_language_callback
from lang_manager import t

ADMIN_USER_ID = 923790989  # Replace with your Telegram user ID

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = handle_start()
    await update.message.reply_text(msg)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = handle_help()
    await update.message.reply_text(msg)

async def topvaults_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/topvaults")
    lang = get_user_settings(update.effective_user.id)["language"]
    message = t("top_vaults", lang)
    await update.message.reply_text(message)

async def setalert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/setalert")
    try:
        user_id = update.effective_user.id
        threshold = float(context.args[0])
        message = handle_set_alert(user_id, threshold)
    except (IndexError, ValueError):
        message = "❌ Usage: /setalert <apy> — e.g. /setalert 40"
    await update.message.reply_text(message)

async def myalert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/myalert")
    user_id = update.effective_user.id
    message = handle_my_alert(user_id)
    await update.message.reply_text(message)

async def removealert_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/removealert")
    user_id = update.effective_user.id
    message = handle_remove_alert(user_id)
    await update.message.reply_text(message)

async def explain_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/explain")
    if not context.args:
        await update.message.reply_text("❓ Usage: /explain <term>")
        return
    term = " ".join(context.args)
    await update.message.reply_text("Looking up explanation...")
    explanation = handle_explain(term)
    await update.message.reply_text(explanation[:4000])

async def define_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Usage: /define <term>")
        return
    term = " ".join(context.args)
    reply = handle_define(term)
    await update.message.reply_text(reply, parse_mode="Markdown")

async def daily_on_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/dailyon")
    reply = handle_daily_on(update.effective_user.id)
    await update.message.reply_text(reply)

async def daily_off_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/dailyoff")
    reply = handle_daily_off(update.effective_user.id)
    await update.message.reply_text(reply)

async def log_summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    track_usage(update.effective_user.id, "/logsummary")
    user_id = update.effective_user.id
    if user_id != ADMIN_USER_ID:
        await update.message.reply_text("🚫 You are not authorized to use this command.")
        return

    summary = handle_log_summary()
    await update.message.reply_text(summary, parse_mode=ParseMode.HTML)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "refresh_market":
        market_data = format_market_data(limit=5)
        keyboard = [
            [InlineKeyboardButton("🔄 Refresh", callback_data="refresh_market")],
            [InlineKeyboardButton("📊 Vaults", callback_data="show_summary")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(market_data[:4000], reply_markup=reply_markup)

    elif query.data == "show_summary":
        summary = generate_summary()
        await query.edit_message_text(summary[:4000])

async def inline_query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query.strip()
    if not query:
        return

    results = search_inline_results(query)
    await update.inline_query.answer(results[:10], cache_time=30)

async def fallback_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer("⚠️ Unknown button.")

async def handle_settings_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    settings = get_user_settings(user_id)

    if query.data == "toggle_digest":
        update_user_setting(user_id, "daily_digest", not settings["daily_digest"])
    elif query.data == "toggle_silent":
        update_user_setting(user_id, "silent_mode", not settings["silent_mode"])
    elif query.data == "edit_threshold":
        context.user_data["awaiting_threshold_input"] = True
        await query.edit_message_text("🔢 Send a new APY alert threshold (e.g., `25`) to update.")
        return

    new_settings = get_user_settings(user_id)
    markup = build_settings_menu(new_settings)
    await query.edit_message_text("⚙️ Updated Settings:", reply_markup=markup)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_threshold_input"):
        try:
            value = float(update.message.text.strip())
            update_user_setting(update.effective_user.id, "alert_threshold", value)
            context.user_data["awaiting_threshold_input"] = False
            await update.message.reply_text(f"✅ Alert threshold set to {value}%")
        except ValueError:
            await update.message.reply_text("❌ Invalid number. Please send a valid APY percentage.")

def run_check_alerts():
    asyncio.run(check_alerts())

def register_handlers(app):
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("topvaults", topvaults_command))
    app.add_handler(CommandHandler("setalert", setalert_command))
    app.add_handler(CommandHandler("myalert", myalert_command))
    app.add_handler(CommandHandler("removealert", removealert_command))
    app.add_handler(CommandHandler("summary", handle_summary))
    app.add_handler(CommandHandler("market", handle_market))
    app.add_handler(CommandHandler("explain", explain_command))
    app.add_handler(CommandHandler("define", define_command))
    app.add_handler(CommandHandler("dailyon", daily_on_command))
    app.add_handler(CommandHandler("dailyoff", daily_off_command))
    app.add_handler(CommandHandler("logsummary", log_summary_command))
    app.add_handler(CommandHandler("settings", handle_settings))
    app.add_handler(CommandHandler("language", handle_language))
    app.add_handler(CallbackQueryHandler(handle_market_pagination, pattern=r"^market_page_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_summary_pagination, pattern=r"^summary_page_\d+$"))
    app.add_handler(CallbackQueryHandler(handle_settings_callback, pattern="^(toggle_digest|toggle_silent|edit_threshold)$"))
    app.add_handler(CallbackQueryHandler(handle_language_callback, pattern=r"^lang_.*$"))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(CallbackQueryHandler(fallback_callback))
    app.add_handler(InlineQueryHandler(inline_query_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
