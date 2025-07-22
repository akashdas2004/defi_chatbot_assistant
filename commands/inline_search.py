from telegram import InlineQueryResultArticle, InputTextMessageContent
import uuid

def search_inline_results(query):
    # Dummy vaults — replace with real DeFi Llama/CoinGecko logic
    data = [
        {"name": "ETH Vault", "apy": "12.5%", "platform": "Yearn"},
        {"name": "BTC Vault", "apy": "9.3%", "platform": "Beefy"},
    ]

    matches = [v for v in data if query.lower() in v["name"].lower()]
    results = []

    for vault in matches:
        text = f"{vault['name']} on {vault['platform']}\nAPY: {vault['apy']}"
        results.append(
            InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"{vault['name']} – {vault['apy']}",
                input_message_content=InputTextMessageContent(text)
            )
        )

    return results 