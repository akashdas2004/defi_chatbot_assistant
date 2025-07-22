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

def get_token_price_changes(symbols):
    """
    Input: ['SOL', 'ETH']
    Output: {'SOL': {'price': 175.2, 'change': -1.2}, ...}
    """
    ids = [i for i in (translate_symbol_to_id(s) for s in symbols) if isinstance(i, str)]
    url = f"{COINGECKO_API_BASE}/coins/markets"
    params = {
        "vs_currency": "usd",
        "ids": ','.join(ids),
        "order": "market_cap_desc",
        "per_page": len(ids),
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            item["symbol"].upper(): {
                "price": item["current_price"],
                "change": item["price_change_percentage_24h"]
            }
            for item in data
        }
    except Exception as e:
        print(f"[CoinGecko API Error] {e}")
        return {}

def get_top_tokens_by_marketcap():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 25, "page": 1}
    res = requests.get(url, params=params)
    tokens = res.json()

    return [
        {
            "symbol": t["symbol"].upper(),
            "name": t["name"],
            "price": t["current_price"],
            "change_24h": t["price_change_percentage_24h"] or 0,
            "market_cap": t["market_cap"]
        }
        for t in tokens
    ]

def translate_symbol_to_id(symbol):
    # NOTE: Mapping may need to be extended
    mapping = {
        "SOL": "solana",
        "ETH": "ethereum",
        "USDC": "usd-coin",
        "USDT": "tether",
        "LINK": "chainlink",
        "AVAX": "avalanche-2",
        "MATIC": "polygon",
    }
    return mapping.get(symbol.upper(), symbol.lower()) 