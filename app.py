import os
import streamlit as st
from dotenv import load_dotenv
from main import topic_already_exists, slugify, rewrite_topic, generate_blog, generate_captions, save_outputs

load_dotenv()

st.set_page_config(page_title="AI Content Creator", layout="wide")
st.title("🧠 AI Content Creator Agent")

topic = st.text_input("Enter a blog topic", "")

# ✅ Slugify and check for duplicates only if topic is typed
if topic:
    slug = slugify(topic)

    # 🔁 Topic already exists? Show rewrite options
    if topic_already_exists(slug):
        st.warning(f"⚠️ Topic '{topic}' already exists.")

        if "rewritten_topic" not in st.session_state or st.session_state.get("last_topic") != topic:
            st.session_state.rewritten_topic = rewrite_topic(topic)
            st.session_state.last_topic = topic

        st.info(f"🔁 Suggested: **{st.session_state.rewritten_topic}**")

        action = st.radio("Choose an action:", ["Skip", "Use Suggested", "Overwrite"])

        if action == "Skip":
            st.stop()
        elif action == "Use Suggested":
            topic = st.session_state.rewritten_topic
            slug = slugify(topic)
            st.success(f"✍️ Final Topic Selected: **{topic}**")

        # Overwrite: do nothing, continue with original topic

st.markdown(f"📌 **Topic to be generated:** `{topic}`")
# ✅ Generate content button (unchanged)
if topic and st.button("Generate Content"):
    with st.spinner("Generating blog and captions..."):

        blog = generate_blog(topic)
        captions = generate_captions(topic)
        save_outputs(topic, blog, captions)

    st.success("✅ Content generated!")

    st.subheader("📝 Blog Post")
    st.markdown(blog)

    st.subheader("📣 Social Media Captions")
    st.text(captions)

    st.download_button("📥 Download Blog (.md)", blog, file_name=f"{topic}.md")
    st.download_button("📥 Download Captions (.txt)", captions, file_name=f"{topic}_captions.txt")
