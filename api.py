from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from agents import writer_agent, proofreader_agent, seo_agent, editor_agent, citation_inserter_agent, social_agent
from utils import estimate_reading_time, generate_tweet_thread, generate_linkedin_post, rewrite_topic, generate_trending_topics, load_blog_calendar_data
from main import topic_already_exists, slugify, generate_blog, generate_captions, save_outputs
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json

app = FastAPI(title="AI Content Creator MCP API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change "*" to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BlogRequest(BaseModel):
    topic: str
    tone: str = "professional"
    audience: str = "general audience"
    outline: str | None = None

class SaveRequest(BaseModel):
    topic: str
    blog: str
    captions: str
    citations: str

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

@app.get("/suggest-topics")
def suggest_topics(category: str = Query(..., example="tech")):
    try:
        topics = generate_trending_topics(category)
        return {"topics": topics.split("\n")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/check-topic")
def check_topic(slug: str, topic: str):
    exists = topic_already_exists(slug)
    suggestion = rewrite_topic(topic)
    return {"exists": exists, "rewritten": suggestion}



@app.post("/save")
def save_blog(req: SaveRequest):
    try:
        save_outputs(req.topic, req.blog, req.captions, req.citations)
        return JSONResponse(content={"message": "Saved successfully"}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/calendar")
def calendar_data():
    df = load_blog_calendar_data()
    return df.to_dict(orient="records")

@app.get("/analytics")
def dashboard_data():
    from datetime import datetime
    import os
    from collections import Counter

    metadata_dir = "metadata"
    all_posts = []

    for filename in os.listdir(metadata_dir):
        if filename.endswith(".json"):
            path = os.path.join(metadata_dir, filename)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                slug = filename.replace(".json", "")
                data["slug"] = slug
                data["date"] = datetime.fromtimestamp(os.path.getmtime(path)).isoformat()
                all_posts.append(data)

    all_tags = [tag for post in all_posts if "seo_tags" in post for tag in post["seo_tags"]]
    unique_tags = list(set(all_tags))

    return {
        "total_blogs": len(all_posts),
        "posts": all_posts,
        "unique_tags": unique_tags,
        "tag_counts": dict(Counter(all_tags))
    }
