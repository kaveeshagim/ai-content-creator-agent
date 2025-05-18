import os
import re
import markdown
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from utils import convert_markdown_to_html, generate_rss_feed,add_topic_to_memory, topic_already_exists,generate_blog_metadata,rewrite_topic,summarize_blog,estimate_reading_time,generate_tweet_thread,generate_linkedin_post,create_share_banner,auto_git_push
from agents import writer_agent, seo_agent, social_agent, editor_agent

# load .env file
load_dotenv()

# get OpenAI API key from environment variable
openai_key = os.getenv("OPENAI_API_KEY")

# initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5, max_tokens=800, openai_api_key=openai_key, )
 
def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

def save_outputs(topic, blog, captions,citations):
    slug = slugify(topic)
    if topic_already_exists(slug):
        print(f"⚠️ Topic '{topic}' already exists.")

        rewritten = rewrite_topic(topic)
        print(f"🔁 Suggested alternative: {rewritten}")
        
        choice = input("(s)kip / (r)egenerate with suggested / (o)verwrite? ").lower()
        if choice == "s":
            print("⏭️ Skipped.")
            return
        elif choice == "r":
            topic = rewritten
            slug = slugify(topic)


    os.makedirs("blogs", exist_ok=True)
    os.makedirs("captions", exist_ok=True)

    with open(f"blogs/{slug}.md", "w", encoding="utf-8") as f:
        f.write(blog)

    with open(f"captions/{slug}_captions.txt", "w", encoding="utf-8") as f:
        f.write(captions)

    print(f"\n✅ Saved blog to blogs/{slug}.md")
    print(f"✅ Saved captions to captions/{slug}_captions.txt")
    convert_markdown_to_html(blog, topic, slug)
    generate_rss_feed()
    add_topic_to_memory(slug)

    # meta = generate_blog_metadata(blog)
    # summary = summarize_blog(blog)

    seo_data = seo_agent(blog)
    socials = social_agent(blog)
    summary = editor_agent(blog)

    try:
        metadata = json.loads(seo_data)
    except json.JSONDecodeError:
        # Try fixing common trailing comma errors
        meta_fixed = re.sub(r",\s*([}\]])", r"\1", seo_data)
        try:
            metadata = json.loads(meta_fixed)
        except json.JSONDecodeError as e:
            print("❌ Failed to parse metadata JSON:", e)
            metadata = {}

    metadata["citations"] = citations or "No citations available."
    metadata["summary_bullets"] = summary
    metadata["reading_time"] = estimate_reading_time(blog)
    metadata["tweet_thread"] = generate_tweet_thread(blog)
    metadata["linkedin_post"] = generate_linkedin_post(blog)
    metadata["share_banner"] = create_share_banner(title=topic, slug=slug)
    metadata["social_posts"] = socials

    os.makedirs("metadata", exist_ok=True)
    with open(f"metadata/{slug}.json", "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"✅ Metadata saved to metadata/{slug}.json")
    auto_git_push()

# function to generate blog content
def generate_blog(topic):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a professional tech blog writer. Your writing should be clear, informative, and easy to understand."),
        ("human", "Write a blog post on the topic: '{topic}'. Include:\n- An engaging introduction\n- Subheadings with clear explanations\n- Bullet points when relevant\n- A strong conclusion.")
    ])

    prompt = prompt_template.format_messages(topic=topic)
    response = llm.invoke(prompt)
    return response.content


def generate_captions(topic):
    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are a social media strategist."),
        ("human", "Create engaging captions for the topic: '{topic}'\nReturn:\n- A short tweet\n- A LinkedIn post\n- An Instagram caption with emojis")
    ])

    prompt = prompt_template.format_messages(topic=topic)
    response = llm.invoke(prompt)
    return response.content

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

    return f"https://kaveeshagim.github.io/ai-content-creator-agent/{slug}.html"  # Update later with real domain

# run this part if the script is executed directly
if __name__ == "__main__":
    topic = input("📌 Enter the topic for the blog post: ")

    # generate blog content
    blog = generate_blog(topic)
    print("\n📝 Generated Blog Post:\n")
    print(blog)

    #generate captions
    captions = generate_captions(topic)
    print("\n📣 Social Media Captions:\n")
    print(captions)

    #save to local files
    save_outputs(topic, blog, captions)