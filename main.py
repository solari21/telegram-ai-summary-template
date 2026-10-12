import os
import sys
import asyncio
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

# Setup readable logging format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("main")

from src.config import validate_config, TIMEZONE, HORAS_ATRAS, COMMUNITY_NAME
from src.telegram_fetcher import fetch_messages_since
from src.summary_generator import generate_summary
from src.card_renderer import render_summary_card
from src.telegram_sender import send_summary_image

def get_slot_info():
    """Calculates active time window and inspection horizon in the community timezone."""
    local_tz = ZoneInfo(TIMEZONE)
    now = datetime.now(local_tz)
    hour = now.hour

    # Manual override from environment (e.g. GitHub Actions workflow_dispatch)
    env_hours = os.environ.get("HORAS_ATRAS")
    if env_hours:
        try:
            h = float(env_hours)
            return f"Manual Run ({now.strftime('%H:%M')} {TIMEZONE})", h
        except ValueError:
            pass

    # Automatic time slot heuristics for scheduled crons (07:00, 14:30, 22:00)
    if 5 <= hour < 11:
        return f"Morning Edition (07:00 {TIMEZONE})", 9.0  # Covering previous night
    elif 11 <= hour < 18:
        return f"Midday Edition (14:30 {TIMEZONE})", 7.5  # Covering morning
    else:
        return f"Evening Edition (22:00 {TIMEZONE})", 7.5 # Covering afternoon

async def run():
    logger.info(f"=== STARTING TELEGRAM AI DIGEST BOT: {COMMUNITY_NAME.upper()} ===")
    validate_config()

    slot_name, hours_back = get_slot_info()
    logger.info(f"Active Slot: {slot_name} | Inspection Horizon: Last {hours_back} hours.")

    # 1. Fetch recent messages via Telegram MTProto
    messages = await fetch_messages_since(hours_back=hours_back)
    if not messages:
        logger.info("No messages found in the inspection window. Workflow concluded.")
        return

    # 2. Generate structured digest with Google Gemini API
    logger.info(f"Generating AI digest for {len(messages)} messages...")
    summary_data = generate_summary(messages, current_slot=slot_name)

    # 3. Render high-resolution infographic card with Playwright
    output_filename = f"output/summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    img_path = await render_summary_card(summary_data, output_path=output_filename)

    # 4. Dispatch infographic to Telegram
    caption = f"🗞️ **{summary_data.get('title', 'COMMUNITY DIGEST')}**\n{summary_data.get('subtitle', '')}\n\n🕒 {slot_name}"
    await send_summary_image(img_path, caption=caption)

    logger.info("=== WORKFLOW SUCCESSFULLY FINISHED ===")

if __name__ == "__main__":
    asyncio.run(run())
