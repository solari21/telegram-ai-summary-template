import os
import sys
import json
import argparse
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

def get_repo_slug():
    repo = os.environ.get("GITHUB_REPOSITORY")
    if repo and "/" in repo:
        return repo.strip()
    return None

def get_github_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token.strip()
    
    auth_file = os.path.expandvars(r"%USERPROFILE%\.gemini\config\mcp-auth\github_token.txt")
    if os.path.exists(auth_file):
        with open(auth_file, "r", encoding="utf-8") as f:
            return f.read().strip()
    return None

def trigger_dispatch(repo_slug: str, workflow_file: str, inputs: dict = None, ref: str = "main"):
    token = get_github_token()
    if not token:
        print("❌ Error: GITHUB_TOKEN not found in environment or local credentials.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo_slug}/actions/workflows/{workflow_file}/dispatches"
    payload = {
        "ref": ref,
        "inputs": inputs or {}
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "User-Agent": "Telegram-AI-Summary-Dispatcher",
            "X-GitHub-Api-Version": "2022-11-28"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status in (204, 201, 200):
                print(f"✅ Workflow '{workflow_file}' triggered successfully on '{repo_slug}' (HTTP {resp.status}).")
                print("⚡ This on-demand dispatch runs immediately, bypassing GitHub Actions cron queues.")
                return True
            else:
                print(f"⚠️ Unexpected response: HTTP {resp.status}")
                return False
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        print(f"❌ HTTP Error {e.code} while dispatching workflow: {err_msg}")
        return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def parse_args():
    parser = argparse.ArgumentParser(description="Instant on-demand GitHub Actions workflow dispatcher")
    parser.add_argument("--repo", type=str, default=None, help="Target repository 'owner/repo' (defaults to GITHUB_REPOSITORY env var)")
    parser.add_argument("--slot", choices=["morning", "midday", "evening", "auto"], default=None, help="Scheduled time slot")
    parser.add_argument("--full-day", action="store_true", help="Trigger 24h full day digest")
    parser.add_argument("--hours", type=str, default=None, help="Trigger manual run looking back N hours")
    parser.add_argument("--custom-title", type=str, default="", help="Optional headline for the digest")
    parser.add_argument("--ref", type=str, default="main", help="Git branch or tag (default: main)")
    return parser.parse_args()

def main():
    args = parse_args()
    repo_slug = args.repo or get_repo_slug()
    if not repo_slug:
        print("❌ Error: Repository slug required! Specify --repo 'owner/repo' or set GITHUB_REPOSITORY.")
        sys.exit(1)

    if args.full_day:
        print(f"🚀 Triggering Full Day Digest on '{repo_slug}' (full_day_summary.yml)...")
        trigger_dispatch(repo_slug, "full_day_summary.yml", ref=args.ref)
    elif args.hours:
        print(f"🚀 Triggering Manual Digest on '{repo_slug}' ({args.hours} hours)...")
        trigger_dispatch(repo_slug, "manual_summary.yml", {
            "hours_back": str(args.hours),
            "custom_title": args.custom_title or ""
        }, ref=args.ref)
    else:
        slot = args.slot or "auto"
        print(f"🚀 Triggering Slot Digest on '{repo_slug}' (daily_summary.yml, slot='{slot}')...")
        trigger_dispatch(repo_slug, "daily_summary.yml", {
            "slot": slot
        }, ref=args.ref)

if __name__ == "__main__":
    main()
