import json
from collections import Counter
from analytics.error_logger import LOG_FILE as ERROR_FILE
from analytics.usage_tracker import USAGE_FILE

def handle_log_summary() -> str:
    try:
        # Load usage logs
        with open(USAGE_FILE, "r") as f:
            usage_data = json.load(f)

        # Count users
        user_ids = {entry["user_id"] for entry in usage_data}
        user_count = len(user_ids)

        # Count top commands
        commands = [entry["command"] for entry in usage_data]
        top_commands = Counter(commands).most_common(3)

        # Load latest error
        with open(ERROR_FILE, "r") as f:
            errors = json.load(f)
        last_error = errors[-1] if errors else None

        # Build the message in HTML
        msg = f"<b>📊 Log Summary</b>\n\n"
        msg += f"👥 <b>Total Users:</b> {user_count}\n\n"

        msg += "<b>📈 Top Commands:</b>\n"
        for cmd, count in top_commands:
            msg += f"- {cmd}: {count} times\n"

        if last_error:
            msg += "\n<b>❌ Last Error:</b>\n"
            msg += f"{last_error['timestamp']}\n"
            msg += f"{last_error['context']} — <code>{last_error['error']}</code>\n"
        else:
            msg += "\n✅ No errors logged."

        return msg

    except Exception as e:
        return f"⚠️ Failed to generate log summary: {e}" 