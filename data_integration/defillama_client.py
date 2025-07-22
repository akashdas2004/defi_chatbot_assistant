import requests

DEFILLAMA_YIELDS_API = "https://yields.llama.fi/pools"

def get_defi_yield_data(limit=10):
    try:
        response = requests.get(DEFILLAMA_YIELDS_API)
        response.raise_for_status()
        data = response.json().get("data", [])
        
        # Filter by highest APY
        sorted_data = sorted(data, key=lambda x: x.get("apy", 0), reverse=True)
        return sorted_data[:limit]
    except Exception as e:
        print(f"[DeFiLlama API Error] {e}")
        return []

def get_top_vaults(limit=5):
    raw_vaults = get_defi_yield_data(limit=limit)
    vaults = []
    for v in raw_vaults:
        # Try to extract symbols from 'symbol' or 'symbols' or fallback to empty list
        symbols = []
        if 'symbols' in v and isinstance(v['symbols'], list):
            symbols = v['symbols']
        elif 'symbol' in v and isinstance(v['symbol'], str):
            # Split on common delimiters
            symbols = [s.strip().upper() for s in v['symbol'].replace('-', '/').split('/') if s.strip()]
        vaults.append({
            'name': v.get('project', v.get('name', 'Unknown Vault')).capitalize(),
            'apy': v.get('apy', 0),
            'chain': v.get('chain', 'N/A'),
            'symbols': symbols
        })
    return vaults 