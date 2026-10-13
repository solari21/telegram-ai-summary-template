import os
import sys
import asyncio
import logging
import argparse
from datetime import datetime
from zoneinfo import ZoneInfo

from .config import validate_config, TIMEZONE, COMMUNITY_NAME
from .telegram_fetcher import fetch_messages_since
from .summary_generator import generate_summary
from .card_renderer import render_summary_card
from .telegram_sender import send_summary_image

logger = logging.getLogger("telegram_ai_summary")

def get_slot_info(custom_hours=None):
    local_tz = ZoneInfo(TIMEZONE)
    now = datetime.now(local_tz)
    hour = now.hour

    if custom_hours is not None:
        return f"Manual Run ({now.strftime('%H:%M')} {TIMEZONE})", float(custom_hours)

    env_hours = os.environ.get("HORAS_ATRAS", "").strip()
    if env_hours:
        try:
            return f"Manual Run ({now.strftime('%H:%M')} {TIMEZONE})", float(env_hours)
        except ValueError:
            pass

    if 5 <= hour < 11:
        return f"Morning Edition (07:00 {TIMEZONE})", 9.0
    elif 11 <= hour < 18:
        return f"Midday Edition (14:30 {TIMEZONE})", 7.5
    else:
        return f"Evening Edition (22:00 {TIMEZONE})", 7.5

async def cmd_run(hours=None, output=None, no_send=False):
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.info(f"=== STARTING TELEGRAM AI DIGEST: {COMMUNITY_NAME.upper()} ===")
    validate_config()

    slot_name, hours_back = get_slot_info(custom_hours=hours)
    logger.info(f"Active Slot: {slot_name} | Inspection Horizon: Last {hours_back} hours.")

    messages = await fetch_messages_since(hours_back=hours_back)
    if not messages:
        logger.info("No messages found in the inspection window. Concluded.")
        return

    logger.info(f"Generating AI digest for {len(messages)} messages with Gemini...")
    summary_data = generate_summary(messages, current_slot=slot_name)

    output_path = output or f"output/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img_path = await render_summary_card(summary_data, output_path=output_path, current_slot=slot_name)

    if not no_send:
        caption = f"🗞️ **{summary_data.get('title', 'COMMUNITY DIGEST')}**\n{summary_data.get('subtitle', '')}\n\n🕒 {slot_name}"
        await send_summary_image(img_path, caption=caption)
    else:
        logger.info(f"--no-send specified. Infographic saved at: {img_path}")

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
    run_parser.add_argument("--hours", type=float, default=None, help="Hours back to inspect")
    run_parser.add_argument("--output", type=str, default=None, help="Output PNG path")
    run_parser.add_argument("--no-send", action="store_true", help="Generate infographic only without sending to Telegram")

    # Command: session
    subparsers.add_parser("session", help="Interactively generate a Telegram StringSession token")

    # Command: demo
    demo_parser = subparsers.add_parser("demo", help="Generate a sample preview infographic without APIs")
    demo_parser.add_argument("--output", type=str, default=None, help="Output PNG path")

    args = parser.parse_args()

    if args.command == "run" or args.command is None:
        hours = getattr(args, "hours", None)
        output = getattr(args, "output", None)
        no_send = getattr(args, "no_send", False)
        asyncio.run(cmd_run(hours=hours, output=output, no_send=no_send))
    elif args.command == "session":
        asyncio.run(cmd_session())
    elif args.command == "demo":
        asyncio.run(cmd_demo(output=args.output))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
