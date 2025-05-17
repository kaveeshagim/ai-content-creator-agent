import os
import schedule
import time
from main import generate_blog, generate_captions, save_outputs
from utils import generate_trending_topics

def auto_generate_blog():
    print("📅 Auto-generation triggered!")
    topics = generate_trending_topics(category="ai").split("\n")
    first_topic = topics[0].lstrip("1234567890. ").strip()

    blog = generate_blog(first_topic)
    captions = generate_captions(blog)
    save_outputs(first_topic, blog, captions)
    print(f"✅ Generated: {first_topic}")

# Schedule once a day at 9 AM
schedule.every().day.at("01:11").do(auto_generate_blog)

print("🕒 Blog Scheduler started... Press Ctrl+C to stop.")
while True:
    schedule.run_pending()
    time.sleep(60)