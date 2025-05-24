import os
import streamlit as st
import json
import pandas as pd
import calplot
from datetime import datetime, timedelta
from google_calendar import create_blog_event
from dotenv import load_dotenv
from main import topic_already_exists, slugify, generate_blog, generate_captions, save_outputs
from utils import rewrite_topic, generate_trending_topics,load_blog_calendar_data
from agents import writer_agent, seo_agent, social_agent, editor_agent, outliner_agent, proofreader_agent, citation_inserter_agent
load_dotenv()

if "blog_queue" not in st.session_state:
    st.session_state.blog_queue = []

st.set_page_config(page_title="AI Content Creator", layout="wide")
st.title("🧠 AI Content Creator Agent")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["✍️ Blog Generator", "📅 Calendar View", "📊 MCP Analytics Dashboard"])

if page == "✍️ Blog Generator":
    topic = st.text_input("Enter a blog topic", st.session_state.get("topic", ""))

    if st.button("➕ Add to Queue"):
        if topic:
            st.session_state.blog_queue.append(topic)
            st.success(f"✅ '{topic}' added to queue!")
        else:
            st.warning("Please enter a topic first.")

    if st.session_state.blog_queue:
        st.markdown("### ⏳ Topics in Queue")
        for i, q_topic in enumerate(st.session_state.blog_queue):
            st.markdown(f"{i+1}. {q_topic}")
    else:
        st.info("Queue is empty.")

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

    if st.session_state.blog_queue:
        with st.form("queue_controls"):
            next_col, full_col = st.columns(2)
            with next_col:
                next_clicked = st.form_submit_button("🚀 Generate Next Topic")
            with full_col:
                full_clicked = st.form_submit_button("🚂 Run Full Queue")

        if next_clicked:
            topic = st.session_state.blog_queue.pop(0)
            st.session_state["topic"] = topic
            st.rerun()

        if full_clicked:
            st.markdown("### ⚙️ Running full queue...")
            while st.session_state.blog_queue:
                queued_topic = st.session_state.blog_queue.pop(0)
                outline_input = None
                raw_blog = writer_agent(queued_topic, tone, audience, outline_input)
                blog = proofreader_agent(raw_blog)
                captions = generate_captions(queued_topic)
                citations = citation_inserter_agent(blog)
                save_outputs(queued_topic, blog, captions, citations)

                # ✅ Schedule on Google Calendar
                # scheduled_time = datetime.now().replace(hour=9, minute=0, second=0) + timedelta(days=1)
                # create_blog_event(queued_topic, scheduled_time)
                # st.info(f"📅 Scheduled '{queued_topic}' for {scheduled_time.strftime('%Y-%m-%d %I:%M %p')}")

                st.success(f"✅ Generated blog for: {queued_topic}")

            st.session_state.blog_queue.clear()
            st.success("🎉 All queued topics have been processed!")


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

        # Load metadata and display details
        meta_path = f"metadata/{slugify(topic)}.json"
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)


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

elif page == "📅 Calendar View":
    st.header("📅 Blog Calendar")

    from utils import load_blog_calendar_data
    df = load_blog_calendar_data()

    if not df.empty:
        df = df.sort_values("date", ascending=False)
        st.dataframe(df[["date", "title"]], use_container_width=True)

        st.markdown("### 🔗 Blog Links")
        for _, row in df.iterrows():
            link = f"[{row['title']}]({f'https://kaveeshagim.github.io/ai-content-creator-agent/{row['slug']}.html'})"
            st.markdown(f"📌 {row['date']}: {link}")
    else:
        st.info("No blogs generated yet.")

elif page == "📊 MCP Analytics Dashboard":
    import matplotlib.pyplot as plt
    from collections import Counter
    from datetime import datetime

    st.header("📊 AI Content Creator Analytics")

    # Load all metadata
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

    export_data = []
    for post in all_posts:
        export_data.append({
            "Title": post.get("slug", "").replace("-", " ").title(),
            "Date": post.get("date").strftime("%Y-%m-%d"),
            "Reading Time": post.get("reading_time", "N/A"),
            "Tags": ", ".join(post.get("seo_tags", [])),
            "Summary": post.get("summary_bullets", ""),
            "Link": f"https://kaveeshagim.github.io/ai-content-creator-agent/{post['slug']}.html"
        })

    df_export = pd.DataFrame(export_data)

    st.success(f"✅ Loaded {len(all_posts)} blog posts")

    # CSV download button
    csv = df_export.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download All Metadata as CSV",
        csv,
        file_name="blog_metadata.csv",
        mime="text/csv"
    )

    st.subheader("📊 Blog Generation Trends")

    # Convert to DataFrame (reusing export_data)
    df_trends = pd.DataFrame(export_data)
    df_trends["Date"] = pd.to_datetime(df_trends["Date"])

    # Group by week
    weekly_counts = df_trends.groupby(pd.Grouper(key="Date", freq="W")).size()
    monthly_counts = df_trends.groupby(pd.Grouper(key="Date", freq="M")).size()

    chart_type = st.radio("View Trends by:", ["Weekly", "Monthly"], horizontal=True)

    if chart_type == "Weekly":
        st.line_chart(weekly_counts, use_container_width=True)
    else:
        st.line_chart(monthly_counts, use_container_width=True)

    # ─────────────────────────────────────
    # 🔹 Summary Metrics
    # ─────────────────────────────────────
    with st.container():
        st.subheader("📈 Overview")
        col1, col2, col3 = st.columns(3)

        col1.metric("📝 Total Blogs", len(all_posts))

        try:
            avg_time = sum(
                int(post["reading_time"].split()[0])
                for post in all_posts if "reading_time" in post
            ) / len(all_posts)
            col2.metric("⏱ Avg Reading Time", f"{round(avg_time)} min")
        except:
            col2.metric("⏱ Avg Reading Time", "N/A")

        all_tags = [
            tag for post in all_posts if "seo_tags" in post for tag in post["seo_tags"]
        ]
        col3.metric("🏷️ Unique Tags", len(set(all_tags)))


    st.subheader("📆 Blog Posting Heatmap")

    # Extract blog post dates
    date_series = [post["date"].date() for post in all_posts]
    df_dates = pd.Series(1, index=pd.to_datetime(date_series))
    df_grouped = df_dates.groupby(df_dates.index).count()

    # ✅ Unpack (fig, ax) from calplot
    fig, _ = calplot.calplot(df_grouped, cmap="YlGnBu", colorbar=True, suptitle="Blog Posts per Day")
    st.pyplot(fig)


    # ─────────────────────────────────────
    # 🔹 SEO Tag Frequency Bar Chart
    # ─────────────────────────────────────
    if all_tags:
        st.subheader("🏷️ Most Common SEO Tags")
        tag_counts = Counter(all_tags).most_common(10)
        tags, counts = zip(*tag_counts)

        fig, ax = plt.subplots()
        ax.barh(tags, counts, color="#4B8BBE")
        ax.set_xlabel("Count")
        ax.set_title("Top SEO Tags")
        st.pyplot(fig)

    # ─────────────────────────────────────
    # 🔹 Filtered Blog Archive
    # ─────────────────────────────────────
    st.subheader("📚 Blog Archive & Filters")

    # ─────────────────────────────────────
    # 🔍 Keyword Search Filter
    # ─────────────────────────────────────
    search_query = st.text_input("🔍 Search by keyword in title or summary")


    # ─────────────────────────────────────
    # 🔎 Filter by SEO Tags
    # ─────────────────────────────────────
    available_tags = sorted(set(all_tags))
    selected_tags = st.multiselect("🏷️ Filter by Tag", available_tags)

    # Sort all posts by date
    all_posts_sorted = sorted(all_posts, key=lambda x: x["date"], reverse=True)

    # First filter by tags
    if selected_tags:
        filtered_posts = [
            post for post in all_posts_sorted
            if any(tag in post.get("seo_tags", []) for tag in selected_tags)
        ]
    else:
        filtered_posts = all_posts_sorted

    # Then apply keyword search on the already tag-filtered posts
    if search_query:
        filtered_posts = [
            post for post in filtered_posts
            if search_query.lower() in post["slug"].lower()
            or search_query.lower() in post.get("summary_bullets", "").lower()
        ]

    st.markdown(f"### 🗂️ Showing {len(filtered_posts)} blog(s)")

    for post in filtered_posts:
        with st.expander(post["slug"].replace("-", " ").title()):
            st.markdown(f"📅 **Date:** {post['date'].strftime('%Y-%m-%d %H:%M')}")
            st.markdown(f"⏱ **Reading Time:** {post.get('reading_time', 'N/A')}")
            st.markdown(f"🏷️ **Tags:** {', '.join(post.get('seo_tags', []))}")
            st.markdown(f"🧠 **Summary:**\n\n{post.get('summary_bullets', 'N/A')}")
            st.markdown(
                f"[🔗 View Blog](https://kaveeshagim.github.io/ai-content-creator-agent/{post['slug']}.html)"
            )
