from data_integration.defillama_client import get_defi_yield_data
from data_integration.coingecko_client import get_top_defi_tokens
from datetime import datetime

def build_digest():
    top_vaults = get_defi_yield_data(limit=2)
    top_tokens = get_top_defi_tokens(limit=3)

    msg = f"📊 *Daily DeFi Digest* ({datetime.now().strftime('%b %d, %Y')})\n\n"

    msg += "🔥 *Top Vaults:*\n"
    for v in top_vaults:
        msg += f"- {v['project'].capitalize()} — {v['apy']:.2f}% APY — {v.get('symbol', '?')} on {v['chain']}\n"

    msg += "\n🚀 *Market Movers:*\n"
    for t in top_tokens:
        change = t.get('price_change_percentage_24h', 0)
        msg += f"- {t['name']}: {change:.2f}%\n"

    msg += "\n🧠 Tip: Use /explain <term> to learn about DeFi terms!"
    return msg 