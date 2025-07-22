import json
import datetime
import os

LOG_FILE = "analytics/error_log.json"

def log_error(error_msg: str, context: str = ""):
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "context": context,
        "error": error_msg,
    }

    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            json.dump([], f)

    with open(LOG_FILE, "r+") as f:
        logs = json.load(f)
        logs.append(log_entry)
        f.seek(0)
        json.dump(logs, f, indent=2)

    print(f"[ERROR] {context}: {error_msg}") 