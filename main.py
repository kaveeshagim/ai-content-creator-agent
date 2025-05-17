import os
import re
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage

# load .env file
load_dotenv()

# get OpenAI API key from environment variable
openai_key = os.getenv("OPENAI_API_KEY")

# initialize the OpenAI chat model
llm = ChatOpenAI(model_name="gpt-4o", temperature=0.5, max_tokens=800, openai_api_key=openai_key, )
 
def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

def save_outputs(topic, blog, captions):
    slug = slugify(topic)
    
    os.makedirs("blogs", exist_ok=True)
    os.makedirs("captions", exist_ok=True)

    with open(f"blogs/{slug}.md", "w", encoding="utf-8") as f:
        f.write(blog)

    with open(f"captions/{slug}_captions.txt", "w", encoding="utf-8") as f:
        f.write(captions)

    print(f"\n✅ Saved blog to blogs/{slug}.md")
    print(f"✅ Saved captions to captions/{slug}_captions.txt")

# function to generate blog content
def generate_blog(topic):
    system_message = SystemMessage(content="You are a professional blog writer who created engaging and informative tech blog posts.")
    human_message = HumanMessage(content=f"Write a detailed blog post about: {topic}. Include an introduction, subheadings, bullet points, main content, and a conclusion. Use a friendly and engaging tone.")

    response = llm([system_message, human_message])
    return response.content

def generate_captions(topic):
    system_message = SystemMessage(content="You are a social media content expert.")
    human_message = HumanMessage(content=f"""Generate engaging captions for the topic: {topic}.
Return:
- A short, catchy tweet (max 280 characters)
- A professional LinkedIn post (2-3 lines)
- A fun Instagram caption with emojis
""")
    response = llm.invoke([system_message, human_message])
    return response.content

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