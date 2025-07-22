from data_integration.defillama_client import get_top_vaults
from data_integration.coingecko_client import get_token_price_changes

def format_defi_summary(vaults, token_prices):
    def format_price(symbol):
        data = token_prices.get(symbol.upper())
        if not data:
            return None
        price = data.get("price", "N/A")
        change = data.get("change", "N/A")
        emoji = "📈" if change >= 0 else "📉"
        return f"${price:.2f} ({emoji} {change:.2f}%)"

    def is_junk_symbol(sym):
        return not sym or sym.upper() in {"W", "X", "Y", "Z", "UNKNOWN"}

    lines = ["📊 *DeFi Market Summary:*\n"]

    for vault in vaults:
        name = vault.get("name", "Unknown Vault")
        apy = vault.get("apy", 0)
        chain = vault.get("chain", "N/A")
        tokens = vault.get("symbols", [])
        token_info_lines = []

        for sym in tokens:
            if is_junk_symbol(sym):
                continue
            price_info = format_price(sym)
            if price_info:
                token_info_lines.append(f"💵 *{sym.upper()}*: {price_info}")

        lines.append(f"💠 *{name}* (`{'-'.join(tokens)}`)")
        lines.append(f"🔗 Chain: {chain}")
        lines.append(f"📈 APY: {apy:,.2f}%")

        if token_info_lines:
            lines.extend(token_info_lines)

        if apy > 1000:
            lines.append("⚠️ *Very high APY* — may be short-lived or risky.")

        lines.append("")  # blank line between vaults

    return "\n".join(lines).strip()

def generate_summary():
    vaults = get_top_vaults(limit=5)
    symbols = list({sym for v in vaults for sym in v.get("symbols", [])})
    token_prices = get_token_price_changes(symbols)
    return format_defi_summary(vaults, token_prices) 