# Task: Structured Outputs & Anti-Crash Resilience (v0.4.1)

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