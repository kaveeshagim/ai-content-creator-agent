from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import writer_agent, proofreader_agent, seo_agent, editor_agent, citation_inserter_agent, social_agent
from utils import estimate_reading_time, generate_tweet_thread, generate_linkedin_post
import json

app = FastAPI(title="AI Content Creator MCP API")

class BlogRequest(BaseModel):
    topic: str
    tone: str = "professional"
    audience: str = "general audience"
    outline: str | None = None

@app.post("/generate")
def generate_blog_content(req: BlogRequest):
    try:
        raw_blog = writer_agent(req.topic, req.tone, req.audience, req.outline)
        blog = proofreader_agent(raw_blog)
        summary = editor_agent(blog)
        citations = citation_inserter_agent(blog)
        seo_data = seo_agent(blog)

        try:
            seo_parsed = json.loads(seo_data)
        except json.JSONDecodeError:
            seo_parsed = {}

        response = {
            "topic": req.topic,
            "raw_blog": raw_blog,
            "blog": blog,
            "summary_bullets": summary,
            "reading_time": estimate_reading_time(blog),
            "citations": citations,
            "seo_tags": seo_parsed.get("seo_tags", []),
            "meta_description": seo_parsed.get("meta_description", ""),
            "tweet_thread": generate_tweet_thread(blog),
            "linkedin_post": generate_linkedin_post(blog),
            "social_posts": social_agent(blog)
        }
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
