import json
import os
from datetime import datetime

USAGE_FILE = "analytics/usage_log.json"

def track_usage(user_id: int, command: str):
    if not os.path.exists(USAGE_FILE):
        with open(USAGE_FILE, "w") as f:
            json.dump([], f)

    with open(USAGE_FILE, "r+") as f:
        data = json.load(f)
        data.append({
            "timestamp": datetime.utcnow().isoformat(),
            "user_id": user_id,
            "command": command
        })
        f.seek(0)
        json.dump(data, f, indent=2) 