import json
from pathlib import Path
import os

ALERTS_FILE = Path("user_profile/alerts.json")

# Load alerts from file
def load_alerts():
    if ALERTS_FILE.exists():
        with open(ALERTS_FILE, "r") as f:
            return json.load(f)
    return {}

# Save alerts to file
def save_alerts(alerts):
    with open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f)

# Public functions
def save_alert_threshold(user_id, threshold):
    alerts = load_alerts()
    alerts[str(user_id)] = threshold
    save_alerts(alerts)

def get_alert_threshold(user_id):
    return load_alerts().get(str(user_id))

def remove_alert(user_id):
    alerts = load_alerts()
    alerts.pop(str(user_id), None)
    save_alerts(alerts)

def get_all_alerts():
    alerts = load_alerts()
    return [(int(uid), apy) for uid, apy in alerts.items()]

USER_FILE = "user_profile/digest_users.json"

def load_digest_users():
    if not os.path.exists(USER_FILE):
        return []
    with open(USER_FILE, "r") as f:
        return json.load(f)

def save_digest_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

def add_digest_user(user_id):
    users = load_digest_users()
    if user_id not in users:
        users.append(user_id)
        save_digest_users(users)

def remove_digest_user(user_id):
    users = load_digest_users()
    if user_id in users:
        users.remove(user_id)
        save_digest_users(users)

SETTINGS_FILE = "user_profile/user_settings.json"

# Load or initialize settings
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_user_settings(user_id):
    settings = load_settings()
    return settings.get(str(user_id), {
        "daily_digest": False,
        "alert_threshold": 50.0,
        "silent_mode": False
    })

def update_user_setting(user_id, key, value):
    settings = load_settings()
    uid = str(user_id)
    if uid not in settings:
        settings[uid] = get_user_settings(user_id)
    settings[uid][key] = value
    save_settings(settings)

def set_language(user_id, lang_code):
    settings = load_settings()
    uid = str(user_id)
    if uid not in settings:
        settings[uid] = get_user_settings(user_id)
    settings[uid]["language"] = lang_code
    save_settings(settings)
