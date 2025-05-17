import os
import json
import streamlit as st
from datetime import datetime

st.set_page_config(page_title="📊 MCP Analytics Dashboard", layout="wide")
st.title("📈 AI Content Creator Analytics")

# Load all metadata files
metadata_dir = "metadata"
all_posts = []

for filename in os.listdir(metadata_dir):
    if filename.endswith(".json"):
        path = os.path.join(metadata_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            slug = filename.replace(".json", "")
            data["slug"] = slug
            data["date"] = datetime.fromtimestamp(os.path.getmtime(path))
            all_posts.append(data)

st.success(f"✅ Loaded {len(all_posts)} posts")

col1, col2, col3 = st.columns(3)

# Total posts
col1.metric("Total Posts", len(all_posts))

# Average reading time
try:
    avg_time = sum(int(post["reading_time"].split()[0]) for post in all_posts if "reading_time" in post) / len(all_posts)
    col2.metric("Avg Reading Time", f"{round(avg_time)} min")
except:
    col2.metric("Avg Reading Time", "N/A")

# Total unique tags
all_tags = [tag for post in all_posts if "seo_tags" in post for tag in post["seo_tags"]]
col3.metric("Unique Tags Used", len(set(all_tags)))

st.markdown("## 📝 Blog Archive")

for post in sorted(all_posts, key=lambda x: x["date"], reverse=True):
    with st.expander(post["slug"].replace("-", " ").title()):
        st.markdown(f"**Date:** {post['date'].strftime('%Y-%m-%d %H:%M')}")
        st.markdown(f"**Reading Time:** {post.get('reading_time', 'N/A')}")
        st.markdown(f"**Tags:** {', '.join(post.get('seo_tags', []))}")
        st.markdown(f"**Summary:**\n\n{post.get('summary_bullets', 'N/A')}")
        if "slug" in post:
            st.markdown(f"[🔗 Read Blog](https://kaveeshagim.github.io/ai-content-creator-agent/{post['slug']}.html)")
