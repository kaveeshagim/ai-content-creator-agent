import yagmail
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("ALERT_EMAIL_USER")
EMAIL_PASS = os.getenv("ALERT_EMAIL_PASS")

def send_devto_alert(post_title, link):
    try:
        yag = yagmail.SMTP(EMAIL_USER, EMAIL_PASS)
        yag.send(
            to=EMAIL_USER,
            subject=f"📬 New Dev.to Draft: {post_title}",
            contents=f"Your blog was picked up and is now in your Dev.to drafts:\n\n{post_title}\n{link}"
        )
        print("✅ Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)
