import os
import schedule
import time
from datetime import datetime
from main import generate_blog, generate_captions, save_outputs
from agents import citation_inserter_agent
from utils import generate_trending_topics
from google_calendar import create_blog_event


def auto_generate_blog():
    print("📅 Auto-generation triggered!")
    topics = generate_trending_topics(category="ai").split("\n")
    first_topic = topics[0].lstrip("1234567890. ").strip()

    blog = generate_blog(first_topic)
    captions = generate_captions(first_topic)
    citations = citation_inserter_agent(blog)
    save_outputs(first_topic, blog, captions, citations)
    print(f"✅ Generated: {first_topic}")

    if os.getenv("ENABLE_GOOGLE_CALENDAR", "false").lower() == "true":
        try:
            create_blog_event(first_topic, datetime.now())
        except Exception as e:
            print("ℹ️ Google Calendar event failed:", e)


# Schedule once a day at 9 AM
schedule.every().day.at("09:00").do(auto_generate_blog)

print("🕒 Blog Scheduler started... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)
