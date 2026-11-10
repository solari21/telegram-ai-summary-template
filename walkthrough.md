# Walkthrough: Versioned Playwright Cache & CI/CD Self-Healing (v0.4.2)

This document certifies the synchronization of the public template `telegram-ai-summary-template` (`v0.4.2`) with the production fix in `reconectados-summary-bot` (`v1.2.2`), resolving `playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist` across GitHub Actions workflows.

---

## 1. 🔍 Root Cause & Fix

- **Root Cause**: `requirements.txt` specifies `playwright>=1.40.0`, so upstream PyPI upgrades install a newer Playwright package while `hashFiles('requirements.txt')` stays unchanged. `actions/cache@v4` hit a stale `~/.cache/ms-playwright` archive and skipped `playwright install --with-deps chromium`.
- **Fix**:
  - Added a `playwright-version` step extracting `playwright --version` into `GITHUB_OUTPUT`.
  - Embedded `${{ steps.playwright-version.outputs.version }}` into the `actions/cache@v4` key.
  - Executed `playwright install --with-deps chromium` unconditionally after cache restore for instant no-op verification and automatic self-healing.

---

# Walkthrough (Historical): Structured Outputs & Anti-Crash Resilience (v0.4.1)

This document certifies the synchronization of the public template `telegram-ai-summary-template` with the production engine enhancements for version `v0.4.1`.

---

## 1. 🚀 Summary of Enhancements

- **Enforced `responseSchema`**: Directly instructs the Gemini API to format its response as a typed JSON object, eliminating unwanted array wrapping from fallback models.
- **Defensive Normalization Pipeline (`normalize_summary_data`)**: Automatically inspects the parsed JSON payload and converts any list or non-dict return into a valid template dictionary with all required keys.
- **Dual-Layer Renderer Shield**: `card_renderer.py` normalizes its input dictionary prior to accessing attributes or rendering Jinja2 templates.
- **Refreshed Model Cascade**: Includes active models (`gemini-3.7-flash`, `gemini-3.6-flash`, `gemini-3.5-flash`, `gemini-3-flash-preview`, `gemini-flash-lite-latest`) with pruned endpoints.
- **Optimized 40s Failover**: Ensures swift model failovers when a primary model encounters heavy load.

---

## 2. 🧪 Verification & Release
- AST clean audit verified with 0 undefined references.
- Packaging verified with wheel and sdist in `dist/`.
- Release `v0.4.1` published on GitHub.