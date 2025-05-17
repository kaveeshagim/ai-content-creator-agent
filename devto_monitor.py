import requests
import time
import os
from email_utils import send_devto_alert


DEV_API_KEY = os.getenv("DEVTO_API_KEY")  # put this in your .env
USERNAME = os.getenv("DEVTO_USERNAME")
headers = {
    "api-key": DEV_API_KEY
}

def check_drafts():
    response = requests.get("https://dev.to/api/articles/me", headers=headers)
    if response.status_code == 200:
        drafts = [post for post in response.json() if not post["published"]]
        print(f"📝 Drafts found: {len(drafts)}")
        for d in drafts[:3]:
            print(f"- {d['title']}")
            send_devto_alert(d['title'], f"https://dev.to/{USERNAME}/{d['slug']}")

    else:
        print("❌ Dev.to API Error:", response.text)

# Auto check every 10 minutes
while True:
    check_drafts()
    time.sleep(600)
