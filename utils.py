import os
import datetime
import markdown
import json
import subprocess
import pandas as pd
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from PIL import Image, ImageDraw, ImageFont

TOPIC_MEMORY_FILE = "memory/topics.json"

def convert_markdown_to_html(markdown_text, title, slug):
    html_content = markdown.markdown(markdown_text)

    # Load metadata
    meta_description = ""
    seo_tags = []
    metadata_path = os.path.join("metadata", f"{slug}.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r", encoding="utf-8") as meta_file:
            try:
                metadata = json.loads(meta_file.read())
                meta_description = metadata.get("meta_description", "")
                seo_tags = metadata.get("seo_tags", [])
            except json.JSONDecodeError:
                pass

    # Themed HTML
    full_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <meta name="description" content="{meta_description}">
        <meta name="keywords" content="{','.join(seo_tags)}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: 'Segoe UI', sans-serif;
                background-color: #fdfdfd;
                color: #222;
                line-height: 1.6;
                padding: 2rem;
                max-width: 700px;
                margin: auto;
            }}
            h1, h2, h3 {{
                color: #111;
                margin-top: 2rem;
            }}
            code {{
                background-color: #f5f5f5;
                padding: 0.2em 0.4em;
                font-family: Consolas, monospace;
                border-radius: 4px;
            }}
            pre {{
                background: #f3f3f3;
                padding: 1rem;
                overflow-x: auto;
                border-radius: 6px;
            }}
            a {{
                color: #007acc;
                text-decoration: none;
            }}
            a:hover {{
                text-decoration: underline;
            }}
            footer {{
                margin-top: 4rem;
                font-size: 0.9em;
                text-align: center;
                color: #888;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        {html_content}
        <footer>
            <p>✨ Generated by the AI Content Creator Agent</p>
        </footer>
    </body>
    </html>
    """

    os.makedirs("docs", exist_ok=True)
    with open(f"docs/{slug}.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    return f"https://kaveeshagim.github.io/ai-content-creator-agent/{slug}.html"


def generate_rss_feed(
    blog_dir="blogs",
    html_dir="docs",
    output="docs/rss.xml",
    site_url="https://kaveeshagim.github.io/ai-content-creator-agent"
):
    rss = Element("rss", {
        "version": "2.0",
        "xmlns:content": "http://purl.org/rss/1.0/modules/content/"
    })

    channel = SubElement(rss, "channel")

    # Feed header
    SubElement(channel, "title").text = "AI Content Creator Blog"
    SubElement(channel, "link").text = site_url
    SubElement(channel, "description").text = "Auto-generated blogs using GPT-4o"

    for filename in os.listdir(blog_dir):
        if filename.endswith(".md"):
            slug = filename[:-3]
            filepath = os.path.join(blog_dir, filename)
            html_link = f"{site_url}/{slug}.html"
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%a, %d %b %Y %H:%M:%S +0530")

            with open(filepath, "r", encoding="utf-8") as f:
                md_content = f.read()

                # Load metadata
                metadata_path = os.path.join("metadata", f"{slug}.json")
                if os.path.exists(metadata_path):
                    with open(metadata_path, "r", encoding="utf-8") as meta_file:
                        try:
                            metadata = json.loads(meta_file.read())
                        except json.JSONDecodeError:
                            metadata = {}
                else:
                    metadata = {}

            title = md_content.splitlines()[0].replace("#", "").strip()
            html_content = markdown.markdown(md_content)

            item = SubElement(channel, "item")
            SubElement(item, "title").text = title
            SubElement(item, "link").text = html_link
            SubElement(item, "pubDate").text = mod_time
            SubElement(item, "guid").text = html_link
            description = metadata.get("meta_description", f"Read full article at {html_link}")
            SubElement(item, "description").text = description
            SubElement(item, "content:encoded").text = f"<![CDATA[{html_content}]]>"
            tags = metadata.get("seo_tags", [])
            for tag in tags:
                SubElement(item, "category").text = tag


    pretty_xml = parseString(tostring(rss)).toprettyxml(indent="  ")
    with open(output, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"✅ RSS feed with content saved as {output}")

def load_topic_memory():
    os.makedirs("memory", exist_ok=True) 
    if not os.path.exists(TOPIC_MEMORY_FILE):
        return []
    with open(TOPIC_MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_topic_memory(topics):
    with open(TOPIC_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(topics, f, indent=2)

def topic_already_exists(slug):
    return slug in load_topic_memory()

def add_topic_to_memory(slug):
    topics = load_topic_memory()
    topics.append(slug)
    save_topic_memory(topics)


def generate_blog_metadata(blog):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an SEO assistant. Output JSON only."),
        ("human", "For the following blog, generate:\n"
                  "- 5 SEO tags (lowercase, no #)\n"
                  "- A meta description (max 160 characters)\n\n"
                  f"Blog:\n{blog}")
    ])

    llm = ChatOpenAI()  # Initialize the LLM (ensure your environment is configured with API keys)
    metadata = llm.invoke(prompt.format_messages())
    return metadata.content

def rewrite_topic(original_topic):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant who rewrites blog topics to avoid duplication."),
        ("human", f"Rewrite the following blog topic to make it unique, catchy, and different:\n\n{original_topic}")
    ])

    llm = ChatOpenAI()
    response = llm.invoke(prompt.format_messages())
    return response.content.strip()

def generate_trending_topics(n=5, category="tech"):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a creative blog strategist. Return a numbered list of blog topic ideas. Keep them timely, relevant, and niche-aligned."),
        ("human", f"Suggest {n} unique, creative, and current blog topics in the '{category}' space.")
    ])

    llm = ChatOpenAI()
    response = llm.invoke(prompt.format_messages())
    return response.content.strip()

def summarize_blog(blog):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an assistant that summarizes blog posts. Output a bullet list of 2–3 short, punchy key points."),
        ("human", f"Summarize this blog post:\n\n{blog}")
    ])

    llm = ChatOpenAI()
    response = llm.invoke(prompt.format_messages())
    return response.content.strip()

def estimate_reading_time(blog_text, wpm=200):
    word_count = len(blog_text.split())
    minutes = max(1, round(word_count / wpm))
    return f"{minutes} min read"

def generate_tweet_thread(blog_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media strategist who converts blogs into engaging Twitter threads. Use short sentences, emojis, and hooks."),
        ("human", f"Convert the following blog into a 5-7 tweet thread:\n\n{blog_text}")
    ])

    llm = ChatOpenAI()
    response = llm.invoke(prompt.format_messages())
    return response.content.strip()

def generate_linkedin_post(blog_text):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media assistant that writes professional LinkedIn posts based on blog content. Include a hook, a 2–3 line summary, emojis, and a soft call-to-action at the end."),
        ("human", f"Write a LinkedIn post based on this blog:\n\n{blog_text}")
    ])

    llm = ChatOpenAI()
    response = llm.invoke(prompt.format_messages())
    return response.content.strip()

from PIL import Image, ImageDraw, ImageFont

def create_share_banner(title, slug):
    os.makedirs("banners", exist_ok=True)

    width, height = 1200, 630
    background_color = (15, 15, 20)  # deep tech gray
    accent_color = (80, 160, 255)    # soft blue

    img = Image.new("RGB", (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    # Load clean sans-serif fonts
    try:
        title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 72)
        footer_font = ImageFont.truetype("DejaVuSans.ttf", 36)
    except:
        title_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # Dynamic title wrapping
    max_width = width - 100
    words = title.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        w = draw.textlength(test_line, font=title_font)
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)

    # Title text positioning
    line_height = title_font.getbbox("A")[3] - title_font.getbbox("A")[1] + 10
    total_height = len(lines) * line_height
    y = (height - total_height) // 2

    for line in lines:
        w = draw.textlength(line, font=title_font)
        x = (width - w) // 2
        draw.text((x, y), line, font=title_font, fill=(240, 240, 240))
        y += line_height

    # Footer
    footer = "⚙️ AI Content Creator"
    fw = draw.textlength(footer, font=footer_font)
    draw.text(((width - fw) // 2, height - 60), footer, font=footer_font, fill=accent_color)

    path = f"banners/{slug}.png"
    img.save(path)
    return path

def auto_git_push():
    try:
        subprocess.run(["git", "add", "docs"], check=True)
        subprocess.run(["git", "commit", "-m", "🤖 Auto update: new blog and RSS"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("✅ Git push complete.")
    except subprocess.CalledProcessError as e:
        print("❌ Git error:", e)

def load_blog_calendar_data():
    records = []
    meta_dir = "metadata"

    for filename in os.listdir(meta_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(meta_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                slug = filename.replace(".json", "")
                date = os.path.getmtime(filepath)  # File modified time
                date_str = datetime.fromtimestamp(date).strftime("%Y-%m-%d")
                title = slug.replace("-", " ").title()
                records.append({"date": date_str, "title": title, "slug": slug})
    
    return pd.DataFrame(records)