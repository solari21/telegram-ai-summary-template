# Windows Task Scheduler Setup for Telegram AI Summary Bot
# Dispatches GitHub Actions workflows via REST API with second-level punctuality.

$pythonPath = (Get-Command python).Source
$scriptPath = Join-Path $PSScriptRoot "trigger_summary.py"

Write-Host "Registering scheduled tasks in Windows Task Scheduler..." -ForegroundColor Cyan

# 1. Morning Edition - 07:00
schtasks /create /tn "Telegram_AI_Summary_Morning" `
    /tr "`"$pythonPath`" `"$scriptPath`" --slot morning" `
    /sc daily /st 07:00 /f | Out-Null
Write-Host "✓ Task 07:00 (Morning) registered." -ForegroundColor Green

# 2. Midday Edition - 14:30
schtasks /create /tn "Telegram_AI_Summary_Midday" `
    /tr "`"$pythonPath`" `"$scriptPath`" --slot midday" `
    /sc daily /st 14:30 /f | Out-Null
Write-Host "✓ Task 14:30 (Midday) registered." -ForegroundColor Green

# 3. Evening Edition - 22:00
schtasks /create /tn "Telegram_AI_Summary_Evening" `
    /tr "`"$pythonPath`" `"$scriptPath`" --slot evening" `
    /sc daily /st 22:00 /f | Out-Null
Write-Host "✓ Task 22:00 (Evening) registered." -ForegroundColor Green

# 4. Full Day Edition - 23:58
schtasks /create /tn "Telegram_AI_Summary_FullDay" `
    /tr "`"$pythonPath`" `"$scriptPath`" --full-day" `
    /sc daily /st 23:58 /f | Out-Null
Write-Host "✓ Task 23:58 (Full Day) registered." -ForegroundColor Green

Write-Host "`nAll tasks successfully registered in Windows Task Scheduler." -ForegroundColor Cyan
