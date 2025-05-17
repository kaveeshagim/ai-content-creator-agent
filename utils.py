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

            title = md_content.splitlines()[0].replace("#", "").strip()
            html_content = markdown.markdown(md_content)

            item = SubElement(channel, "item")
            SubElement(item, "title").text = title
            SubElement(item, "link").text = html_link
            SubElement(item, "pubDate").text = mod_time
            SubElement(item, "guid").text = html_link
            SubElement(item, "description").text = f"Read full article at {html_link}"
            SubElement(item, "content:encoded").text = f"<![CDATA[{html_content}]]>"

    pretty_xml = parseString(tostring(rss)).toprettyxml(indent="  ")
    with open(output, "w", encoding="utf-8") as f:
        f.write(pretty_xml)

    print(f"✅ RSS feed with content saved as {output}")