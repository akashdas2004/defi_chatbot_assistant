import requests

COINGECKO_API_BASE = "https://api.coingecko.com/api/v3"

def get_top_defi_tokens(limit=5):
    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "category": "decentralized-finance-defi",
        "order": "market_cap_desc",
        "per_page": limit,
        "page": 1
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] CoinGecko API failed: {e}")
        return []

def format_market_data(limit=5):
    tokens = get_top_defi_tokens(limit=limit)

    if not tokens:
        return "⚠️ Could not fetch market data at the moment."

    result = "📈 Top DeFi Tokens by Market Cap:\n\n"
    for token in tokens:
        name = token.get("name")
        symbol = token.get("symbol").upper()
        price = token.get("current_price", 0)
        change = token.get("price_change_percentage_24h", 0)
        mcap = token.get("market_cap", 0)

        emoji = "📈" if change > 0 else "📉"
        result += (
            f"• {name} ({symbol})\n"
            f"  Price: ${price:.2f} ({emoji} {change:.2f}%)\n"
            f"  Market Cap: ${mcap:,.0f}\n\n"
        )

    return result 