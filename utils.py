import os
import datetime
import markdown
from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom.minidom import parseString

def convert_markdown_to_html(markdown_text, title, slug):
    html_content = markdown.markdown(markdown_text)

    # Basic HTML wrapper (can improve later)
    full_html = f"""
    <html>
    <head>
        <title>{title}</title>
        <meta charset="UTF-8">
    </head>
    <body>
        <h1>{title}</h1>
        {html_content}
    </body>
    </html>
    """

    # Save it
    os.makedirs("docs", exist_ok=True)
    with open(f"docs/{slug}.html", "w", encoding="utf-8") as f:
        f.write(full_html)

    return f"https://kaveeshagim.github.io/ai-content-creator-agent/{slug}.html"

def generate_rss_feed(blog_dir="blogs", html_dir="public_html", output="rss.xml", site_url="https://kaveeshagim.github.io/ai-content-creator-agent"):
    rss = Element("rss", version="2.0")
    channel = SubElement(rss, "channel")

    # Feed header
    SubElement(channel, "title").text = "AI Content Creator Blog"
    SubElement(channel, "link").text = site_url
    SubElement(channel, "description").text = "Auto-generated blogs using GPT-4o"

    for filename in os.listdir(blog_dir):
        if filename.endswith(".md"):
            slug = filename[:-3]
            html_link = f"{site_url}/{slug}.html"

            # Get file modified time as pubDate
            filepath = os.path.join(blog_dir, filename)
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).strftime("%a, %d %b %Y %H:%M:%S +0530")

            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                title = lines[0].replace("#", "").strip() if lines else slug

            item = SubElement(channel, "item")
            SubElement(item, "title").text = title
            SubElement(item, "link").text = html_link
            SubElement(item, "pubDate").text = mod_time
            SubElement(item, "description").text = f"Read full article at {html_link}"

    # Save to rss.xml
    pretty_xml = parseString(tostring(rss)).toprettyxml(indent="  ")
    with open("docs/rss.xml", "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"✅ RSS feed saved as {output}")