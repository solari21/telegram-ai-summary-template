# 🚀 Telegram AI Daily Summary Bot & Infographic Generator

<p align="left">
  <a href="README.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-Switch-blue?style=flat&logo=googletranslate&logoColor=white" height="20" alt="Cambiar a Español" /></a>
  &nbsp;
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-Active-orange?style=flat&logo=readme&logoColor=white" height="20" alt="Active English Version" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg?style=flat&logo=python&logoColor=white" height="20" alt="Python Version" />
  &nbsp;
  <a href="https://github.com/solari21/telegram-ai-summary-template/releases/tag/v0.3.0"><img src="https://img.shields.io/badge/release-v0.3.0-blue.svg?style=flat&logo=github" height="20" alt="Release v0.3.0" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/REA%20MCP-Web%20Stability-success?style=flat&logo=shield&logoColor=white" height="20" alt="REA MCP Web Stability" />
  &nbsp;
  <img src="https://img.shields.io/badge/automation-GitHub_Actions-2088FF.svg?style=flat&logo=github-actions&logoColor=white" height="20" alt="GitHub Actions" />
  &nbsp;
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat" height="20" alt="License MIT" />
</p>

> **Transform active Telegram groups and gaming communities into visually stunning dark-mode infographics with humorous AI-generated daily recaps. Available as both an automated Serverless Template and an installable Python CLI package.**

---

## 📸 Infographic Preview

Real sample of the high-definition infographic automatically rendered by this bot:

<p align="center">
  <img src="assets/demo_summary.png" alt="Demo Infographic Telegram AI Daily Summary" width="700">
</p>

---

## ✨ Key Features

- ⚡ **100% Serverless & Free**: Runs via scheduled crons on GitHub Actions. Zero VPS, zero hosting costs, and zero servers running 24/7.
- 📅 **Triple Execution Mode**:
  1. **Slot-Based Summaries**: Morning (07:00), Midday (14:30), and Evening (22:00) with dynamic subtitles and fixed inspection windows.
  2. **Full-Day Summary**: Midnight recap covering 24 full hours (00:00 to 23:59).
  3. **On-Demand Manual Trigger**: Dispatch anytime from GitHub Actions or CLI with custom relative hours (e.g., 2, 4, 8, 12, 24, 48) and titles.
- 🧠 **5-Model AI Cascade with Exponential Backoff**: Built for cutting-edge **Google Gemini 3.8 Flash**, with automated retries (3s / 6s backoff) and graceful fallback to **3.5 Flash**, **3.5 Flash Lite**, **2.0 Flash**, and **2.0 Flash Lite** during server traffic spikes (503 / 500 / 429).
- 🎨 **Web Stability & Razor-Sharp Rendering (REA MCP Integration)**: Custom Jinja2 HTML5/CSS3 template rendered with Playwright Chromium at 2x Retina scale. Integrates **REA MCP** web execution stabilization (`document.fonts.ready` & double `requestAnimationFrame`), preventing layout shifts and pixelated font fallbacks.
- 🔐 **Zero-Leak Architecture**: Uses Telethon `StringSession` and encrypted GitHub Actions Secrets. No SQLite session database files on disk.
- 🕒 **Smart Timezone Detection**: Automatically calculates inspection windows and converts timestamps to your local timezone (e.g., `Europe/Madrid`).
- 🛠️ **Open, Reusable Template**: Zero private tokens, chat IDs, or messages hardcoded. Ready to clone, configure, and deploy in under 5 minutes.

---

## 🏛️ System Architecture & Workflow

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/architecture-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/architecture-light.svg">
    <img alt="Telegram AI Daily Summary Architecture & Flow" src="assets/architecture.svg" width="950">
  </picture>
</p>

---

## 📅 GitHub Actions Automation Modes

The template includes **3 production-ready workflows**:

### 1. Slot-Based Digest (`daily_summary.yml`)
Runs automatically 3 times a day on offset minutes (`:02` and `:32`) to avoid GitHub Actions runner queue congestion on the hour:
* **07:00 Local** (05:02 UTC in daylight saving): Fixed window **22:00 (yesterday) to 07:00 (today)**.
* **14:30 Local** (12:32 UTC in daylight saving): Fixed window **07:00 to 14:30 (today)**.
* **22:00 Local** (20:02 UTC in daylight saving): Fixed window **14:30 to 22:00 (today)**.

### 2. Full 24-Hour Day Digest (`full_day_summary.yml`)
* Dispatches every night at **23:58 Madrid** (21:58 UTC).
* Gathers **the entire day (00:00:00 to 23:59:59)** and generates the complete daily debrief.

### 3. On-Demand Manual Trigger (`manual_summary.yml`)
* Interactive generation via the GitHub Actions tab, selecting hours to inspect and an optional custom title.

---

## 🚀 3-Step Quick Deployment

### 1. Click "Use this template"
Create your own private or public repository from this template on GitHub.

### 2. Configure Repository Secrets
In your GitHub repository, navigate to **Settings > Secrets and variables > Actions** and add:
- `TELEGRAM_API_ID`: Your Telegram API ID (from https://my.telegram.org).
- `TELEGRAM_API_HASH`: Your Telegram API Hash.
- `TELEGRAM_STRING_SESSION`: The Telethon string session (generate it using `python tools/generate_string_session.py`).
- `TELEGRAM_CHAT_ID`: The ID of the Telegram group to summarize (e.g., `-1001234567890`).
- `TELEGRAM_SEND_TO`: `me` (for Saved Messages) or the numeric ID of the recipient channel/group.
- `GEMINI_API_KEY`: Your Google AI Studio API Key (free tier supported).

### 3. Ready to Go!
Your workflows will trigger on schedule or whenever launched manually.

---

## 📦 Python CLI Package Usage

You can also install and run this project as a standard Python CLI tool:

```bash
pip install .
telegram-ai-summary --demo  # Generates a demo infographic without requiring credentials
```

---

## 🛡️ Credits & Acknowledgments

- **REA MCP (`rea-agents@6.7.0`)**: Web execution analysis, static audit patterns, and typography stabilization.
- **Google Gemini**: Multimodal models for conversational synthesis and comedic tone analysis.
- **Telethon**: Asynchronous MTProto Telegram client.
- **Playwright**: High-resolution headless Chromium rendering engine.

---

## 📋 Project Management & Roadmap

- 📌 **GitHub Projects V2 Kanban Board**: [Telegram AI Digest Roadmap](https://github.com/users/solari21/projects/1)
- 📝 **Milestone Checklist**: [TODO.md](TODO.md)

---

## 📄 License

Published under the [MIT License](LICENSE).
