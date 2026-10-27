# Task: Time Slot Resilience, Playwright Browser Caching & CET Timezone Parity (v0.4.0)

## Objective
Harmonize the public template with production fixes: eliminate quota starvation on manual triggers using `offset_date`, clamp interactive executions to current time, guarantee delivery during quiet periods, cache Playwright browser binaries to accelerate CI/CD, and align scheduled crons with winter CET time (UTC+1).

## Checklist
- [x] 1. `offset_date` extraction in Telethon client.
- [x] 2. Dynamic window clamping for interactive runs.
- [x] 3. Guaranteed contingency infographic for zero-message windows.
- [x] 4. Playwright caching (`actions/cache@v4` on `~/.cache/ms-playwright`) and 20m timeout.
- [x] 5. Winter CET timezone alignment (UTC+1).
- [x] 6. Clean AST audit (`verify_ast_clean.py`).
- [x] 7. Build wheel and source distributions in `dist/`.
- [x] 8. Semantic bump to `v0.4.0` and official GitHub Release.
