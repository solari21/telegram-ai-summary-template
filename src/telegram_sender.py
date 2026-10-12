import logging
from telethon import TelegramClient
from telethon.sessions import StringSession

from src.config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_STRING_SESSION,
    TELEGRAM_SEND_TO
)

logger = logging.getLogger("telegram_sender")

def resolve_target(target_str: str):
    if not target_str or target_str.lower() == "me":
        return "me"
    try:
        return int(target_str)
    except ValueError:
        return target_str

async def send_summary_image(image_path: str, caption: str = ""):
    """
    Uploads and sends the summary card PNG to the designated recipient
    ('me' for Saved Messages, or a specific group/channel chat ID).
    """
    destination = resolve_target(TELEGRAM_SEND_TO)
    logger.info(f"Connecting to Telegram MTProto to send summary to '{destination}'...")

    client = TelegramClient(StringSession(TELEGRAM_STRING_SESSION), TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.connect()

    try:
        if not await client.is_user_authorized():
            raise PermissionError("Telegram session unauthorized. Please check TELEGRAM_STRING_SESSION.")

        target_entity = await client.get_input_entity(destination)
        msg = await client.send_file(
            target_entity,
            file=image_path,
            caption=caption,
            parse_mode="markdown"
        )
        logger.info(f"Summary image sent successfully! Message ID: {msg.id}")
        return msg
    finally:
        await client.disconnect()
