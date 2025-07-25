import os
import requests

COINMARKETCAP_API_KEY = os.environ.get("COINMARKETCAP_API_KEY")

def get_top_tokens_by_marketcap(limit=50, convert="USD"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
    }
    params = {
        "start": 1,
        "limit": limit,
        "convert": convert,
    }

    try:
        response = requests.get(url, headers=headers, params=params)

        print("[CMC] Status Code:", response.status_code)
        if response.status_code != 200:
            print("[CMC ERROR] Non-200 response:", response.text)
            return []

        data = response.json()
        if "data" not in data:
            print("[CMC ERROR] 'data' not in response:", data)
            return []

        tokens = []
        for item in data["data"]:
            quote = item["quote"][convert]
            tokens.append({
                "name": item["name"],
                "symbol": item["symbol"],
                "price": quote["price"],
                "change_24h": quote["percent_change_24h"],
                "market_cap": quote["market_cap"]
            })

        print(f"[CMC] Retrieved {len(tokens)} tokens")
        return tokens

    except Exception as e:
        print("[CMC EXCEPTION]", str(e))
        return []
def get_market_data(symbol="BTC", currency="USD"):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": COINMARKETCAP_API_KEY,
    }
    params = {
        "symbol": symbol,
        "convert": currency,
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if "data" not in data:
            print("[CMC QUOTE ERROR] No 'data':", data)
            return {}
        return data
    except Exception as e:
        print("[CMC QUOTE EXCEPTION]", str(e))
        return {}

print("[DEBUG] API KEY:", COINMARKETCAP_API_KEY)
