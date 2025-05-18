import os
import streamlit as st
import json
from dotenv import load_dotenv
from main import topic_already_exists, slugify, generate_blog, generate_captions, save_outputs
from utils import rewrite_topic, generate_trending_topics
from agents import writer_agent, seo_agent, social_agent, editor_agent, outliner_agent, proofreader_agent, citation_inserter_agent
load_dotenv()

st.set_page_config(page_title="AI Content Creator", layout="wide")
st.title("🧠 AI Content Creator Agent")

topic = st.text_input("Enter a blog topic", st.session_state.get("topic", ""))
tone = st.selectbox(
    "Select tone/style",
    ["professional", "casual", "witty", "inspirational", "conversational"],
    index=0
)
audience = st.selectbox(
    "Select target audience",
    ["general audience", "beginners", "developers", "business professionals", "CTOs", "students"],
    index=0
)

if topic:
    if st.checkbox("🧠 Show AI-generated outline before writing"):
        from agents import outliner_agent

        with st.spinner("Thinking through the structure..."):
            generated_outline = outliner_agent(topic, audience)
            outline_input = st.text_area("📋 Edit Outline", value=generated_outline, height=300)


with st.expander("📈 Need ideas? Generate trending topics"):
    category = st.selectbox("Choose category", ["tech", "ai", "devops", "startups", "webdev"])
    
    if st.button("Suggest Topics"):
        with st.spinner("Thinking of hot blog ideas..."):
            topic_list = generate_trending_topics(category=category)
            st.session_state.suggested_topics = topic_list.split("\n")

    if "suggested_topics" in st.session_state:
        for i, suggestion in enumerate(st.session_state.suggested_topics):
            cleaned = suggestion.lstrip("1234567890. ").strip()
            if st.button(f"Use: {cleaned}", key=f"suggest-{i}"):
                st.session_state["topic"] = cleaned
                try:
                    st.rerun()
                except AttributeError:
                    st.experimental_rerun()


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

# ✅ Generate content button (unchanged)
if topic and st.button("Generate Content"):
    with st.spinner("Generating blog and captions..."):

        # blog = generate_blog(topic)
        if "outline_input" not in locals():
            outline_input = None

        raw_blog = writer_agent(topic, tone, audience, outline_input)
        blog = proofreader_agent(raw_blog)
        citations = citation_inserter_agent(blog)
        captions = generate_captions(topic)

        save_outputs(topic, blog, captions,citations)

    st.success("✅ Content generated!")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("✍️ Raw Draft (Writer Agent)")
        st.markdown(raw_blog)

    with col2:
        st.subheader("🧼 Polished Draft (Proofreader Agent)")
        st.markdown(blog)

    st.subheader("📝 Blog Post")
    st.markdown(blog)

    # Show reading time if available
    meta_path = f"metadata/{slugify(topic)}.json"
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            data = json.load(f)

            # if "reading_time" in data:
            #     st.caption(f"⏱ {data['reading_time']}")

    # st.subheader("📣 Social Media Captions")
    # st.text(captions)

        if "reading_time" in data:
            st.caption(f"⏱ {data['reading_time']}")

        if "citations" in data:
            st.subheader("🔗 Suggested Citations")
            st.markdown(data["citations"])
                
        if "summary_bullets" in data:
            st.subheader("📌 Blog Summary")
            st.markdown(data["summary_bullets"])

        st.subheader("📣 Social Media Captions")
        st.text(captions)

        if "tweet_thread" in data:
            st.subheader("🐦 Tweet Thread")
            st.text(data["tweet_thread"])
            st.download_button("📥 Download Tweet Thread (.txt)", data["tweet_thread"], file_name=f"{slugify(topic)}_thread.txt")

        if "linkedin_post" in data:
            st.subheader("📰 LinkedIn Post")
            st.text_area("Preview", data["linkedin_post"], height=200)
            st.download_button("📥 Download LinkedIn Post (.txt)", data["linkedin_post"], file_name=f"{slugify(topic)}_linkedin.txt")

        if "share_banner" in data and os.path.exists(data["share_banner"]):
            st.subheader("🖼️ Social Share Banner")
            st.image(data["share_banner"])
            with open(data["share_banner"], "rb") as f:
                st.download_button("📥 Download Banner (.png)", f, file_name=f"{slugify(topic)}.png")

    st.download_button("📥 Download Blog (.md)", blog, file_name=f"{topic}.md")
    st.download_button("📥 Download Captions (.txt)", captions, file_name=f"{topic}_captions.txt")
