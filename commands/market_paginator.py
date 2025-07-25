from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Update
from telegram.ext import ContextTypes
from data_integration.coinmarketcap_client import get_top_tokens_by_marketcap  # ← updated

TOKENS_PER_PAGE = 5

def get_page_data(tokens, page):
    start = (page - 1) * TOKENS_PER_PAGE
    end = start + TOKENS_PER_PAGE
    total_pages = (len(tokens) + TOKENS_PER_PAGE - 1) // TOKENS_PER_PAGE

    formatted = f"📈 *Top Tokens by Market Cap (Page {page}/{total_pages}):*\n\n"
    for token in tokens[start:end]:
        price = token.get("price", 0)
        change = token.get("change_24h", 0)
        symbol = token["symbol"]
        name = token["name"]
        mcap = f"${int(token.get('market_cap', 0)):,}"
        emoji = "📈" if change >= 0 else "📉"

        formatted += (
            f"• *{name}* ({symbol})\n"
            f"  Price: ${price:.2f} ({emoji} {change:.2f}%)\n"
            f"  Market Cap: {mcap}\n\n"
        )

    return formatted.strip()

def build_keyboard(page, max_pages):
    buttons = []
    if page > 1:
        buttons.append(InlineKeyboardButton("⬅️ Prev", callback_data=f"market_page_{page-1}"))
    if page < max_pages:
        buttons.append(InlineKeyboardButton("➡️ Next", callback_data=f"market_page_{page+1}"))
    return InlineKeyboardMarkup([buttons]) if buttons else None

async def handle_market(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tokens = get_top_tokens_by_marketcap(limit=50)  # ← CoinMarketCap returns top tokens
    context.user_data["market_tokens"] = tokens  # cache for pagination
    text = get_page_data(tokens, 1)
    reply_markup = build_keyboard(1, (len(tokens) + TOKENS_PER_PAGE - 1) // TOKENS_PER_PAGE)

    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=reply_markup)

async def handle_market_pagination(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    page = int(query.data.split("_")[-1])
    tokens = context.user_data.get("market_tokens")

    if not tokens:
        tokens = get_top_tokens_by_marketcap(limit=50)
        context.user_data["market_tokens"] = tokens

    text = get_page_data(tokens, page)
    markup = build_keyboard(page, (len(tokens) + TOKENS_PER_PAGE - 1) // TOKENS_PER_PAGE)

    await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=markup)
