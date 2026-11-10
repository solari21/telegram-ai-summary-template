# Task: Versioned Playwright Cache & CI/CD Self-Healing (v0.4.2)

## Objective
Prevent `BrowserType.launch: Executable doesn't exist` errors across all GitHub Actions workflows (`daily_summary.yml`, `full_day_summary.yml`, `manual_summary.yml`) when `playwright>=1.40.0` updates upstream on PyPI without changing `requirements.txt`.

## Checklist (v0.4.2)
- [x] 1. Forensic root-cause analysis on stale `actions/cache@v4` key (`hashFiles('requirements.txt')`).
- [x] 2. Added `playwright-version` step capturing `playwright --version` into `GITHUB_OUTPUT`.
- [x] 3. Versioned `actions/cache@v4` key with `${{ steps.playwright-version.outputs.version }}`.
- [x] 4. Unconditional `playwright install --with-deps chromium` verification after cache restore.
- [x] 5. Built wheel and source distributions in `dist/` for `0.4.2` and validated AST cleanliness.
- [x] 6. Bilingual docs parity (`README.md`, `README_EN.md`, `TODO.md`, `walkthrough.md`), Release `v0.4.2` and Projects V2 Done.

---

# Task (Historical): Structured Outputs & Anti-Crash Resilience (v0.4.1)

## Objective
Harmonize the public template with production fixes: eliminate `AttributeError: 'list' object has no attribute 'get'` by enforcing `responseSchema` in the Gemini API and introducing a universal defensive normalization layer in both summary generation and card rendering.

## Checklist
- [x] 1. `responseSchema` specification in Gemini API `generationConfig`.
- [x] 2. Defensive `normalize_summary_data` helper handling lists, wrapped dicts, and missing keys.
- [x] 3. Double-layer protection in `card_renderer.py`.
- [x] 4. Refreshed active candidate models cascade (`gemini-3.7-flash`, `gemini-3.6-flash`, etc.).
- [x] 5. Trimmed socket read timeout to 40s.
- [x] 6. Clean AST audit (`verify_ast_clean.py`).
- [x] 7. Build wheel and source distributions in `dist/`.
- [x] 8. Semantic bump to `v0.4.1` and official GitHub Release.