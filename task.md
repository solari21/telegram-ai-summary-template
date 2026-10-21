# Task: REA MCP Web Stability Integration (v0.3.0)

## Objective
Integrate REA MCP web execution stability patterns into the Playwright infographic renderer, ensure font hydration without FOUT (Flash of Unstyled Text), eliminate layout shifts in CSS Grid, update documentation, rebuild distributions, and publish release v0.3.0.

## Atomic Checklist
- [x] 1. Update `src/telegram_ai_summary/card_renderer.py` with `document.fonts.ready` and double `requestAnimationFrame`.
- [x] 2. Clean up misplaced files in `src/`.
- [x] 3. Verify clean AST across package modules (`verify_ast_clean.py`).
- [x] 4. Bump version to 0.3.0 in `pyproject.toml`.
- [x] 5. Synchronize `README.md` and `README_EN.md` with REA credits and SVG badge compliance.
- [x] 6. Update `TODO.md` roadmap.
- [x] 7. Build source and wheel distributions in `dist/`.
- [x] 8. Commit, push, and create GitHub Release `v0.3.0`.
