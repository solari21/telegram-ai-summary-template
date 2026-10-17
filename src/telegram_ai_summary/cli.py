import os
import sys
import asyncio
import logging
import argparse
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from .config import validate_config, TIMEZONE, COMMUNITY_NAME
from .telegram_fetcher import fetch_messages_since
from .summary_generator import generate_summary
from .card_renderer import render_summary_card
from .telegram_sender import send_summary_image

logger = logging.getLogger("telegram_ai_summary")

def resolve_execution_plan(args=None):
    """
    Decoupled calculation of slot identity, title, and exact fixed time window
    in the configured timezone (e.g. Europe/Madrid), guaranteeing absolute
    congruence against runner queue delays in GitHub Actions or cloud schedulers.
    """
    local_tz = ZoneInfo(TIMEZONE)
    now = datetime.now(local_tz)

    cli_slot = getattr(args, "slot", None) if args else None
    cli_cron = getattr(args, "cron_trigger", None) if args else None
    cli_hours = getattr(args, "hours", None) if args else None
    cli_full_day = getattr(args, "full_day", False) if args else False
    cli_title = getattr(args, "custom_title", None) if args else None
    cli_dry_run = getattr(args, "dry_run", False) or getattr(args, "no_send", False) if args else False
    cli_output = getattr(args, "output", None) if args else None

    env_slot = (
        os.environ.get("SLOT") or
        os.environ.get("INPUT_SLOT") or
        os.environ.get("PAYLOAD_SLOT") or
        ""
    ).strip().lower()

    env_cron = (
        os.environ.get("GITHUB_EVENT_SCHEDULE") or
        os.environ.get("GITHUB_CRON_TRIGGER") or
        ""
    ).strip()

    env_action = os.environ.get("GITHUB_EVENT_ACTION", "").strip().lower()
    env_mode = os.environ.get("MODE", "").strip().lower()
    env_full_day = os.environ.get("FULL_DAY", "").strip().lower() in ("true", "1", "yes")
    env_hours = os.environ.get("HORAS_ATRAS", "").strip()
    env_title = os.environ.get("CUSTOM_TITLE", "").strip()

    title_tag = cli_title or env_title or None

    raw_slot = (cli_slot or env_slot).lower()
    if raw_slot == "auto":
        raw_slot = ""

    slot_aliases = {
        "matinal": "morning",
        "mediodia": "midday",
        "nocturna": "evening",
        "night": "evening",
        "dia-completo": "full-day",
        "fullday": "full-day"
    }
    target_slot = slot_aliases.get(raw_slot, raw_slot)

    # Autodetect from repository_dispatch event_type
    if not target_slot and env_action:
        if "morning" in env_action or "matinal" in env_action:
            target_slot = "morning"
        elif "midday" in env_action or "mediodia" in env_action:
            target_slot = "midday"
        elif "night" in env_action or "nocturna" in env_action or "evening" in env_action:
            target_slot = "evening"
        elif "full_day" in env_action or "dia_completo" in env_action:
            target_slot = "full-day"

    # Autodetect from cron schedule expression
    active_cron = cli_cron or env_cron
    if not target_slot and active_cron:
        clean_cron = " ".join(active_cron.split())
        if clean_cron in ("2 5 * * *", "0 5 * * *", "5 5 * * *"):
            target_slot = "morning"
        elif clean_cron in ("32 12 * * *", "30 12 * * *", "0 12 * * *"):
            target_slot = "midday"
        elif clean_cron in ("2 20 * * *", "0 20 * * *", "20 20 * * *"):
            target_slot = "evening"
        elif clean_cron in ("58 21 * * *", "59 21 * * *", "0 22 * * *"):
            target_slot = "full-day"

    # Full day mode check
    is_full_day = (
        target_slot == "full-day" or
        bool(cli_full_day) or
        env_full_day or
        env_mode == "full-day"
    )

    if is_full_day:
        if now.hour < 6:
            target_date = (now - timedelta(days=1)).date()
        else:
            target_date = now.date()
        start_time = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=local_tz)
        end_time = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, 999999, tzinfo=local_tz)
        suffix = f": {title_tag}" if title_tag else ""
        slot_name = f"Full Day Edition{suffix} ({target_date.strftime('%d/%m/%Y')} {TIMEZONE})"
        return {
            "slot": "full-day",
            "slot_name": slot_name,
            "hours_back": 24.0,
            "is_full_day": True,
            "start_time": start_time,
            "end_time": end_time,
            "custom_title": title_tag,
            "dry_run": cli_dry_run,
            "output": cli_output
        }

    # Manual mode check
    effective_hours = cli_hours or env_hours
    if effective_hours is not None or target_slot == "manual":
        try:
            h_float = float(effective_hours) if effective_hours else 8.0
        except ValueError:
            h_float = 8.0
        start_time = now - timedelta(hours=h_float)
        end_time = now
        suffix = f": {title_tag}" if title_tag else ""
        slot_name = f"Manual Run{suffix} ({start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')} {TIMEZONE})"
        return {
            "slot": "manual",
            "slot_name": slot_name,
            "hours_back": h_float,
            "is_full_day": False,
            "start_time": start_time,
            "end_time": end_time,
            "custom_title": title_tag,
            "dry_run": cli_dry_run,
            "output": cli_output
        }

    # Fallback to current time if no explicit slot provided
    if not target_slot:
        hour = now.hour
        if 5 <= hour < 11:
            target_slot = "morning"
        elif 11 <= hour < 18:
            target_slot = "midday"
        else:
            target_slot = "evening"

    today = now.date()
    yesterday = today - timedelta(days=1)

    if target_slot == "morning":
        start_time = datetime(yesterday.year, yesterday.month, yesterday.day, 22, 0, 0, tzinfo=local_tz)
        end_time = datetime(today.year, today.month, today.day, 7, 0, 0, tzinfo=local_tz)
        slot_name = f"Morning Edition (07:00 {TIMEZONE})"
        hours_back = 9.0
    elif target_slot == "midday":
        start_time = datetime(today.year, today.month, today.day, 7, 0, 0, tzinfo=local_tz)
        end_time = datetime(today.year, today.month, today.day, 14, 30, 0, tzinfo=local_tz)
        slot_name = f"Midday Edition (14:30 {TIMEZONE})"
        hours_back = 7.5
    else:  # evening
        if now.hour < 6:
            # Runner started past midnight: analyze yesterday's evening
            target_d = yesterday
        else:
            target_d = today
        start_time = datetime(target_d.year, target_d.month, target_d.day, 14, 30, 0, tzinfo=local_tz)
        end_time = datetime(target_d.year, target_d.month, target_d.day, 22, 0, 0, tzinfo=local_tz)
        slot_name = f"Evening Edition (22:00 {TIMEZONE})"
        hours_back = 7.5

    if title_tag:
        slot_name += f" - {title_tag}"

    return {
        "slot": target_slot,
        "slot_name": slot_name,
        "hours_back": hours_back,
        "is_full_day": False,
        "start_time": start_time,
        "end_time": end_time,
        "custom_title": title_tag,
        "dry_run": cli_dry_run,
        "output": cli_output
    }

async def cmd_run(args=None):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info(f"=== STARTING TELEGRAM AI DIGEST: {COMMUNITY_NAME.upper()} ===")
    validate_config()

    plan = resolve_execution_plan(args)
    logger.info(
        f"Execution Plan: Slot '{plan['slot']}' | Name: '{plan['slot_name']}' | "
        f"Window: {plan['start_time'].strftime('%Y-%m-%d %H:%M')} to {plan['end_time'].strftime('%Y-%m-%d %H:%M')} {TIMEZONE} "
        f"(Full Day: {plan['is_full_day']}, Dry Run: {plan['dry_run']})"
    )

    messages = await fetch_messages_since(
        hours_back=plan["hours_back"],
        full_day=plan["is_full_day"],
        start_time_local=plan["start_time"],
        end_time_local=plan["end_time"]
    )
    if not messages:
        logger.info("No messages found in the inspection window. Concluded.")
        return

    logger.info(f"Generating AI digest for {len(messages)} messages with Gemini...")
    summary_data = generate_summary(messages, current_slot=plan["slot_name"])

    if plan["custom_title"]:
        summary_data["title"] = plan["custom_title"].upper()

    output_path = plan["output"] or f"output/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img_path = await render_summary_card(summary_data, output_path=output_path, current_slot=plan["slot_name"])

    if not plan["dry_run"]:
        caption = f"🗞️ **{summary_data.get('title', 'COMMUNITY DIGEST')}**\n{summary_data.get('subtitle', '')}\n\n🕒 {plan['slot_name']}"
        await send_summary_image(img_path, caption=caption)
    else:
        logger.info(f"Dry-run / no-send active. Infographic successfully saved at: {img_path}")

    logger.info("=== WORKFLOW SUCCESSFULLY FINISHED ===")

async def cmd_session():
    from telethon import TelegramClient
    from telethon.sessions import StringSession

    print("=" * 65)
    print(" 🚀 TELEGRAM STRING SESSION GENERATOR")
    print("=" * 65)
    print("Get your API credentials for free at: https://my.telegram.org\n")

    api_id_input = input("Enter your TELEGRAM_API_ID: ").strip()
    api_hash_input = input("Enter your TELEGRAM_API_HASH: ").strip()

    if not api_id_input or not api_hash_input:
        print("\n❌ Error: API ID and API Hash are required!")
        sys.exit(1)

    try:
        api_id = int(api_id_input)
    except ValueError:
        print("\n❌ Error: API ID must be an integer!")
        sys.exit(1)

    print("\nConnecting to Telegram... (You will receive an official login code)")
    client = TelegramClient(StringSession(), api_id, api_hash_input)

    await client.start()
    session_string = client.session.save()
    me = await client.get_me()
    await client.disconnect()

    print("\n" + "=" * 65)
    print(f"✅ Login successful for: {me.first_name} (@{me.username or 'NoUsername'})")
    print("=" * 65)
    print("\n🔑 YOUR TELEGRAM_STRING_SESSION (Copy everything below):\n")
    print(session_string)
    print("\n" + "=" * 65)
    print("⚠️  KEEP THIS SECRET! Anyone with this string can access your Telegram account.")
    print("Add this string to your repository's GitHub Secrets or your local .env file.")
    print("=" * 65 + "\n")

async def cmd_demo(output=None):
    from .mock_data import MOCK_SUMMARY
    out = output or "assets/demo_summary.png"
    print(f"Rendering demo card to {out}...")
    await render_summary_card(MOCK_SUMMARY, output_path=out)
    print(f"✅ Demo card rendered at: {out}")

def main():
    parser = argparse.ArgumentParser(
        prog="telegram-ai-summary",
        description="AI-powered infographic daily digest generator for Telegram communities."
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: run
    run_parser = subparsers.add_parser("run", help="Fetch messages, generate digest, render card and dispatch to Telegram")
    def clean_arg(val):
        if not val:
            return None
        cleaned = str(val).strip().strip("'\"")
        return cleaned if cleaned else None

    run_parser.add_argument(
        "--slot",
        type=clean_arg,
        default=None,
        help="Explicit time slot to execute (morning, midday, evening, full-day, manual, auto)"
    )
    run_parser.add_argument("--cron-trigger", type=clean_arg, default=None, help="Cron expression that triggered the workflow")
    run_parser.add_argument("--hours", type=float, default=None, help="Hours back to inspect in manual mode")
    run_parser.add_argument("--full-day", action="store_true", help="Fetch full day messages (00:00 to 23:59)")
    run_parser.add_argument("--custom-title", type=str, default=None, help="Custom headline for the digest")
    run_parser.add_argument("--output", type=str, default=None, help="Output PNG path")
    run_parser.add_argument("--dry-run", action="store_true", help="Generate infographic without dispatching to Telegram")
    run_parser.add_argument("--no-send", action="store_true", help="Alias for --dry-run")

    # Command: session
    subparsers.add_parser("session", help="Interactively generate a Telegram StringSession token")

    # Command: demo
    demo_parser = subparsers.add_parser("demo", help="Generate a sample preview infographic without APIs")
    demo_parser.add_argument("--output", type=str, default=None, help="Output PNG path")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        asyncio.run(cmd_run(args))
    elif args.command == "session":
        asyncio.run(cmd_session())
    elif args.command == "demo":
        asyncio.run(cmd_demo(output=args.output))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
