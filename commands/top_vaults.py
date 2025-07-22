from data_integration.defillama_client import get_defi_yield_data

def get_top_vaults_text(limit=5):
    vaults = get_defi_yield_data(limit=limit)

    if not vaults:
        return "⚠️ Could not fetch vaults at the moment."

    result = "🌾 Top Yield Farming Vaults:\n\n"
    for v in vaults:
        result += (
            f"• Protocol: {v['project'].capitalize()}\n"
            f"  Chain: {v['chain']}\n"
            f"  Symbol: {v.get('symbol', '?')}\n"
            f"  APY: {v['apy']:.2f}%\n\n"
        )
    return result 