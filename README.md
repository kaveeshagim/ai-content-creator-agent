# 🧠 AI Content Creator Agent

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-%23FAAC58?logo=chainlink&logoColor=black)
![OpenAI GPT-4o](https://img.shields.io/badge/OpenAI-GPT--4o-blueviolet?logo=openai)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-222?logo=github)](https://kaveeshagim.github.io/ai-content-creator-agent/)
![RSS Feed](https://img.shields.io/badge/Auto--Publishing-Dev.to-orange?logo=devdotto)
![Medium](https://img.shields.io/badge/Supports-Medium%20Import-green?logo=medium)
![Last Updated](https://img.shields.io/github/last-commit/kaveeshagim/ai-content-creator-agent)
![License](https://img.shields.io/github/license/kaveeshagim/ai-content-creator-agent)

> An intelligent, agent-powered blog generator built with Python, LangChain, and OpenAI GPT-4o. Fully automated — from idea to published blog with zero manual effort.

---

### ✨ Key Features

- 🔍 Input any blog topic
- 🧠 Outliner Agent to structure posts before writing
- ✍️ Writer Agent + Proofreader Agent for high-quality content
- 📣 Auto-generated captions for Twitter, LinkedIn, Instagram
- 🔗 Citation Inserter Agent for credibility and references
- 🎯 SEO Agent for tags, meta descriptions, and summaries
- 🖼️ Share Banner Generator for social media branding
- 💾 Saves content as `.md`, `.txt`, `.json`, and `.html`
- 📤 Auto-push to GitHub Pages for hosting + RSS feed
- 📰 Auto-publish to Dev.to via RSS
- 🎛️ Streamlit UI with queue system, trending topics, outline editing
- 📊 Built-in Analytics Dashboard (reading time, tags, calendar heatmap)

---

### 🧩 Modular Agent Architecture

| Agent               | Role                                                      |
| ------------------- | --------------------------------------------------------- |
| `Outliner Agent`    | Creates blog structure before writing                     |
| `Writer Agent`      | Generates content based on topic, tone, audience, outline |
| `Proofreader Agent` | Cleans and refines blog content                           |
| `Citation Agent`    | Inserts credible references and links                     |
| `SEO Agent`         | Suggests meta description and SEO tags                    |
| `Social Agent`      | Generates captions and post templates for each platform   |
| `Editor Agent`      | Summarizes content in bullet points                       |

---

### 🖥️ Streamlit UI Features

- ✅ Topic input, tone & audience selector
- 📋 Optional outline preview and editing
- ➕ Queue multiple topics for batch processing
- 🚀 One-click generation with live feedback
- 📦 Downloadable files and preview windows
- 📆 Analytics Dashboard with:
  - Calendar heatmap
  - Weekly/monthly trends
  - Top tags
  - Filterable blog archive
  - CSV export

---

### 📂 Project Structure

- 📁 `blogs/` → Markdown blog posts
- 📁 `captions/` → Captions for each blog
- 📁 `metadata/` → Blog metadata (JSON: SEO, summary, links, etc.)
- 📁 `docs/` → GitHub Pages folder (.html files + rss.xml)
- 📁 `banners/` → Social share images
- 📄 `rss.xml` → Auto-updated RSS feed for Dev.to and Medium

---

### 🔮 Possible Enhancements

- 🧵 Thread Composer Agent (Twitter carousel style)
- 📱 Mobile version using Streamlit Cloud / Flutter
- 🧠 Personalization agent for tone & voice calibration
- 🤖 Slack + Zapier integration for daily blog triggers
- 📨 Newsletter bot for Substack / Revue

---

### 📡 Live Demo

- 🌍 [GitHub Pages Blog Feed](https://kaveeshagim.github.io/ai-content-creator-agent/)
- 📰 [Auto-published to Dev.to](https://dev.to/kaveesha_c74582728492e034)

---

### 🛠️ Tech Stack

- Python 3.11
- LangChain
- OpenAI GPT-4o
- Streamlit
- Matplotlib + Calplot
- GitHub Pages + RSS

---

Want to build your own AI-powered publishing assistant?  
**Fork this repo and start generating!**

---
