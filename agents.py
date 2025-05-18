from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# def writer_agent(topic):
#     prompt_template = ChatPromptTemplate.from_messages([
#         ("system", "You are a professional tech blog writer. Your writing should be clear, informative, and easy to understand."),
#         ("human", "Write a blog post on the topic: '{topic}'. Include:\n- An engaging introduction\n- Subheadings with clear explanations\n- Bullet points when relevant\n- A strong conclusion.")
#     ])

#     prompt = prompt_template.format_messages(topic=topic)
#     response = llm.invoke(prompt)
#     return response.content

def writer_agent(topic, tone="professional", audience="general audience", outline=None):
    messages = [
        ("system", f"You are a {tone} technical blog writer for {audience}. Your job is to write clear, helpful, and engaging content.")
    ]

    if outline:
        messages.append((
            "human",
            f"Write a blog based on this outline:\n\n{outline}"
        ))
    else:
        messages.append((
            "human",
            f"Write a blog on the topic: {topic}. Include:\n"
            "- A compelling introduction\n"
            "- Multiple subheadings\n"
            "- Bullet points where useful\n"
            "- A strong closing summary."
        ))

    prompt = ChatPromptTemplate.from_messages(messages)
    return llm.invoke(prompt.format_messages()).content.strip()



def seo_agent(blog):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an SEO expert. Output JSON only."),
        ("human", f"Give me 5 lowercase SEO tags and a 160-character meta description for this blog:\n\n{blog}")
    ])
    return llm.invoke(prompt.format_messages()).content.strip()

def social_agent(blog):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a social media expert."),
        ("human", f"Turn the following blog into a tweet thread and a LinkedIn post:\n\n{blog}")
    ])
    return llm.invoke(prompt.format_messages()).content.strip()

def editor_agent(blog):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a blog editor."),
        ("human", f"Summarize this blog in 3 bullet points:\n\n{blog}")
    ])
    return llm.invoke(prompt.format_messages()).content.strip()

def outliner_agent(topic, audience="general audience"):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"You are a blog planning assistant for {audience}."),
        ("human", f"Create a detailed outline for a blog titled: '{topic}'. "
                  f"Include an intro, 3–5 main sections, and 2–3 bullet points under each.")
    ])
    return llm.invoke(prompt.format_messages()).content.strip()

def proofreader_agent(blog):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a professional blog proofreader and editor. Improve grammar, clarity, and flow without changing the meaning or tone."),
        ("human", f"Proofread and polish the following blog content:\n\n{blog}")
    ])
    return llm.invoke(prompt.format_messages()).content.strip()
