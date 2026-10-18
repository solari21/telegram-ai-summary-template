# 📋 Project Status & Roadmap (TODO & Milestones)

Living tracking document for the implementation status, verified production milestones, and upcoming roadmap for **Telegram AI Summary Bot Template**.

---

## ✅ Completed Milestones (100% Production Ready & Tested)

### 1. Telegram MTProto Data Fetcher
- [x] **Native MTProto client via Telethon & StringSession**: Secure user-account message collection without requiring third-party bot tokens.
- [x] **Strict timezone normalization**: UTC timestamps converted to target community timezone (`TIMEZONE` setting, defaulting to `Europe/Madrid`).
- [x] **Decoupled Fixed Time Windows**: Exact clock-window inspection horizons (Morning: 22:00 to 07:00, Midday: 07:00 to 14:30, Evening: 14:30 to 22:00, Full-Day: 00:00 to 23:59). Even if a runner experiences hours of delay, content, timestamps and titles remain 100% accurate without drift or mislabeling.
- [x] **Multi-mode inspection horizons**: Supports relative time horizons (`--hours N`), automatic slot windows, and 24-hour calendar days (`--full-day`).
- [x] **Midnight Boundary Resilience**: Automatic detection for early morning executions (00:00 - 05:59 local time), targeting **yesterday's full calendar day** (00:00:00 to 23:59:59) to prevent empty digests caused by GitHub Actions queue delays.
- [x] **Dynamic slot window expansion**: Gracefully extends the inspection horizon backwards if runner queues delay the evening run past midnight.

### 2. AI Digest Engine (Google Gemini)
- [x] **5-Model Resilience Cascade**:
  1. `gemini-3.8-flash` (Primary: maximum reasoning and wit).
  2. `gemini-3.5-flash` (Fallback 1: high speed and quality).
  3. `gemini-3.5-flash-lite` (Fallback 2: lightweight efficiency).
  4. `gemini-2.0-flash` (Fallback 3: high availability).
  5. `gemini-2.0-flash-lite` (Fallback 4: ultimate continuity fallback).
- [x] **Exponential backoff retries**: Up to 2 retries with 3s and 6s intervals for transient Google API errors (HTTP 503 / 500 / 429).
- [x] **Contextual dynamic subtitles**: Automatically tailored to morning, midday, evening, full-day, or manual runs.
- [x] **Custom titles support**: Easily add custom headlines (`--custom-title "EVENT NAME"`).

### 3. Visual Infographic Rendering & Delivery
- [x] **HTML/CSS dark mode gamer card**: Jinja2 templated with dynamic category badges and responsive typography.
- [x] **Headless Playwright Chromium renderer**: Ultra-crisp Retina x2 device scale factor capture.
- [x] **Automated Telegram delivery**: Delivers rendered PNG directly to Telegram Saved Messages (`'me'`) or configurable chat.

### 4. Serverless GitHub Actions Workflows & Cloud Schedulers
- [x] **Triple workflow architecture**:
  - `daily_summary.yml`: Automated slot digests (07:00, 14:30, 22:00 local) with interactive dropdown selector (`slot: midday | morning | evening | auto`) and `repository_dispatch` webhooks.
  - `full_day_summary.yml`: Automated 24-hour full-day digest (23:58 local) with `repository_dispatch`.
  - `manual_summary.yml`: Interactive on-demand dispatch with custom parameters (`hours_back`, `custom_title`) and `repository_dispatch`.
- [x] **100% Cloud Webhook Automation (cron-job.org compatibility)**: Full support for external cloud schedulers via GitHub `repository_dispatch` API to bypass GitHub Actions cron queue delays entirely.
- [x] **Instant CLI Dispatch Utility (`tools/trigger_summary.py`)**: Trigger any workflow from local terminal with zero delay.
- [x] **Anti-congestion off-peak cron minutes**: Configured at minutes `:02`, `:32`, and `:58` to bypass global GitHub Actions top-of-the-hour queue drops.
- [x] **Template-safe secrets guard**: Workflow step guard `if [ -z "$TELEGRAM_STRING_SESSION" ]` gracefully skips runs on upstream template repository without failing when secrets are not configured, maintaining 100% green status on forks and templates.
- [x] **Python 3.11 strict f-string compatibility (Rule II.24)**: Extracted backslashes outside f-string expressions in card rendering for flawless execution across all Python versions on Ubuntu GitHub runners.
- [x] **CLI empty argument sanitization (`clean_arg`)**: Universal argument sanitizer ensuring empty strings in scheduled/webhook triggers do not cause CLI parsing errors.
- [x] **Node 24 upgrade**: Replaced deprecated actions with `actions/checkout@v6` and `setup-python@v6` for zero-warning runs.
- [x] **Editable Python package layout**: Standard `src/` distribution with `pip install -e .` and console entrypoint `telegram-ai-summary`.
- [x] **Official GitHub Release v0.2.1**: Published [v0.2.1](https://github.com/solari21/telegram-ai-summary-template/releases/tag/v0.2.1) with precompiled wheels (`.whl`), Diagram Design architecture SVGs/PNGs, and dual-badge language switcher.
- [x] **Previous Release v0.2.0**: Published [v0.2.0](https://github.com/solari21/telegram-ai-summary-template/releases/tag/v0.2.0) with precompiled wheel (`.whl`) and source distribution (`.tar.gz`) attached via automated CI/CD.
- [x] **Strict Bilingual Parity (`README.md` & `README_ES.md`)**: Complete technical documentation in English and Spanish with interactive top switcher.
- [x] **Editorial Architecture Diagram (`diagram-design`)**: High-fidelity dark/light/universal SVGs and Retina @2x PNGs embedded with responsive `<picture>` tags.
- [x] **Transversal 1:1 Parity with Production Bot (`reconectados-summary-bot`)**: Full synchronization of features, helper tools, and assets.
- [x] **Configurable destination target (`TELEGRAM_SEND_TO`)**: Custom channel or group chat ID routing.

---

## 🚀 Upcoming Roadmap (Planned Enhancements)

### Near Term
- [ ] **Text-only fallback**: Send markdown text directly if Playwright dependencies fail in lightweight container environments.
- [ ] **Interactive session generator wizard CLI**: Enhanced step-by-step terminal prompt for 2FA-protected accounts.

### Medium Term
- [ ] **Multi-theme support**: Add switchable CSS templates (*Modern Light*, *Cyberpunk*, *Minimalist Editorial*).
- [ ] **Community leaderboard**: Highlight top contributors, most used emojis, and message volume metrics in the footer.
- [ ] **Voice message transcription**: Process short Telegram voice notes using Gemini multimodal audio capabilities.
- [ ] **Docker containerization**: Pre-built Docker image for self-hosted cron runs on VPS, NAS or local servers.
