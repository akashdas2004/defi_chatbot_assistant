from data_integration.coinmarketcap_client import get_market_data

# Default list of tokens
DEFAULT_TOP_TOKENS = ["BTC", "ETH", "SOL", "BNB", "ADA"]
DEFAULT_CURRENCY = "USD"

def get_top_tokens_cmc(symbols=DEFAULT_TOP_TOKENS, currency=DEFAULT_CURRENCY):
    """
    Fetches market data for given symbols from CoinMarketCap.
    """
    data = get_market_data(",".join(symbols), currency=currency)
    if not data or "data" not in data:
        return None

    tokens = []
    for symbol in symbols:
        token = data["data"].get(symbol)
        if token:
            try:
                quote = token["quote"][currency]
                tokens.append({
                    "name": token["name"],
                    "symbol": symbol.upper(),
                    "price": quote["price"],
                    "change": quote["percent_change_24h"],
                    "market_cap": quote["market_cap"]
                })
            except KeyError:
                continue
    return tokens


def format_market_data(symbols=DEFAULT_TOP_TOKENS, limit=5, currency=DEFAULT_CURRENCY):
    """
    Formats the top token data for display.
    """
    tokens = get_top_tokens_cmc(symbols[:limit], currency=currency)
    if not tokens:
        return "⚠️ Could not fetch market data at the moment."

    currency_sign = "$" if currency.upper() == "USD" else f"{currency.upper()} "
    result = f"📈 Top Tokens by Market Cap ({currency.upper()}):\n\n"

    for token in tokens:
        name = token["name"]
        symbol = token["symbol"]
        price = token["price"]
        change = token["change"]
        mcap = token["market_cap"]
        emoji = "📈" if change > 0 else "📉"
        result += (
            f"• {name} ({symbol})\n"
            f"  Price: {currency_sign}{price:,.2f} ({emoji} {change:.2f}%)\n"
            f"  Market Cap: {currency_sign}{mcap:,.0f}\n\n"
        )
    return result
