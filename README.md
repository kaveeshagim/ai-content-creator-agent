# 🧠 AI Content Creator Agent

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-%23FAAC58?logo=chainlink&logoColor=black)
![OpenAI GPT-4o](https://img.shields.io/badge/OpenAI-GPT--4o-blueviolet?logo=openai)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-222?logo=github)](https://ccxxcc.github.io/ai-content-creator-agent/)
![RSS Feed](https://img.shields.io/badge/Auto--Publishing-Dev.to-orange?logo=devdotto)
![Medium](https://img.shields.io/badge/Supports-Medium%20Import-green?logo=medium)
![Last Updated](https://img.shields.io/github/last-commit/ccxxcc/ai-content-creator-agent)
![License](https://img.shields.io/github/license/ccxxcc/ai-content-creator-agent)

This is an intelligent content generation agent built with Python, LangChain, and OpenAI GPT-4o. It allows you to:

- 🔍 Input any topic
- ✍️ Automatically generate a full blog post
- 📣 Create social media captions for Twitter, LinkedIn, and Instagram
- 💾 Save everything locally as `.md`, `.txt`, and `.html` files
- 🌐 Host content using GitHub Pages and generate a live RSS feed
- 📰 Auto-publish blog posts to Dev.to via RSS
- 🧠 Powered by GPT-4o for high-quality results

### 🚀 Features

- Uses LangChain + OpenAI for AI-generated blog content
- Clean prompt templates for consistent tone and structure
- RSS feed (`rss.xml`) includes full blog HTML content for Dev.to
- Streamlit UI to easily input topics and generate results
- Medium-friendly: import blog URLs manually
- Dev.to-friendly: automatic detection and publishing via RSS

### 📦 Output Structure

- `blogs/` — Markdown blog content
- `captions/` — Social media caption sets
- `docs/` — GitHub Pages folder with `.html` blogs and `rss.xml`

### 🔮 Future Enhancements

- 🧰 Agent memory to track topics and avoid duplication
- 🧠 AI-powered SEO and meta description suggestions
- 📬 Newsletter generation + Substack/Buttondown integration
- 🧵 Auto-thread generator for Twitter posts
- 🎨 Themed HTML styling and Dark Mode export
