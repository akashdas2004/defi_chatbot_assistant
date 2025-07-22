from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from data_integration.defillama_client import get_top_vaults
from data_integration.coingecko_client import get_token_price_changes
from commands.summary import format_defi_summary

TOKENS_PER_PAGE = 5

def get_summary_page(vaults, prices, page):
    total_pages = (len(vaults) + TOKENS_PER_PAGE - 1) // TOKENS_PER_PAGE
    start = (page - 1) * TOKENS_PER_PAGE
    end = start + TOKENS_PER_PAGE
    sliced = vaults[start:end]
    text = format_defi_summary(sliced, prices)
    return text, total_pages

def build_summary_keyboard(page, total_pages):
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"summary_page_{page-1}"))
    if page < total_pages:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"summary_page_{page+1}"))
    return InlineKeyboardMarkup([buttons]) if buttons else None

async def handle_summary(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vaults = get_top_vaults(limit=25)
    symbols = list({sym for v in vaults for sym in v.get("symbols", [])})
    prices = get_token_price_changes(symbols)
    context.user_data["summary_data"] = (vaults, prices)

    page = 1
    text, total_pages = get_summary_page(vaults, prices, page)
    markup = build_summary_keyboard(page, total_pages)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=markup)

async def handle_summary_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    page = int(query.data.split("_")[-1])

    vaults, prices = context.user_data.get("summary_data", ([], {}))
    if not vaults:
        vaults = get_top_vaults(limit=25)
        symbols = list({sym for v in vaults for sym in v.get("symbols", [])})
        prices = get_token_price_changes(symbols)
        context.user_data["summary_data"] = (vaults, prices)

    text, total_pages = get_summary_page(vaults, prices, page)
    markup = build_summary_keyboard(page, total_pages)
    await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=markup) 