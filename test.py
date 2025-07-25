import requests

API_KEY = "2e1e9839-7887-4913-86c7-c1e2c8d7b1f6"  # 🔁 Replace this with your real key
BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"

def test_coinmarketcap_api(symbol="BTC", convert="USD"):
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": API_KEY
    }
    params = {
        "symbol": symbol,
        "convert": convert
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "data" in data and symbol in data["data"]:
            price = data["data"][symbol]["quote"][convert]["price"]
            print(f"✅ API is working. {symbol} price in {convert}: ${price:,.2f}")
        else:
            print("⚠️ API response structure unexpected:", data)

    except requests.exceptions.RequestException as e:
        print("❌ API request failed:", e)

# Run test
if __name__ == "__main__":
    test_coinmarketcap_api()
