from data_integration.defillama_client import get_defi_yield_data
from user_profile.profile_manager import get_all_alerts
from alerts.notification_dispatcher import send_alert

# Simple notification tracking to avoid spam
notification_history = {}

def should_notify(user_id, key):
    """Prevent spam by tracking recent notifications"""
    global notification_history
    current_key = f"{user_id}:{key}"
    import time
    current_time = time.time()
    
    # Clean old entries (older than 1 hour)
    notification_history = {k: v for k, v in notification_history.items() 
                          if current_time - v < 3600}
    
    if current_key in notification_history:
        return False
    
    notification_history[current_key] = current_time
    return True

async def check_alerts():
    alerts = get_all_alerts()
    top_vaults = get_defi_yield_data(limit=10)

    for user_id, threshold in alerts:
        for vault in top_vaults:
            apy = vault.get("apy", 0)
            if apy > threshold:
                key = f"{vault['project']}:{vault.get('symbol', '?')}"
                message = (
                    f"🚨 Yield Alert!\n"
                    f"{vault['project']} on {vault['chain']} is now {apy:.2f}% APY"
                )
                if should_notify(user_id, key):
                    await send_alert(user_id, message)
