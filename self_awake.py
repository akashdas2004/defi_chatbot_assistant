import os
import time
import requests

SELF_AWAKE_URL = os.environ.get("SELF_AWAKE_URL")  # Set this to your Render app URL

if not SELF_AWAKE_URL:
    raise ValueError("SELF_AWAKE_URL environment variable not set.")

def ping():
    try:
        response = requests.get(SELF_AWAKE_URL)
        print(f"Pinged {SELF_AWAKE_URL}: {response.status_code}")
    except Exception as e:
        print(f"Failed to ping {SELF_AWAKE_URL}: {e}")

if __name__ == "__main__":
    while True:
        ping()
        time.sleep(600)  # Ping every 10 minutes