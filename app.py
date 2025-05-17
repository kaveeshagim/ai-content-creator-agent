import os
import streamlit as st
from dotenv import load_dotenv
from main import generate_blog, generate_captions, save_outputs

load_dotenv()

st.set_page_config(page_title="AI Content Creator", layout="wide")
st.title("🧠 AI Content Creator Agent")

topic = st.text_input("Enter a blog topic", "")

if topic:
    if st.button("Generate Content"):
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