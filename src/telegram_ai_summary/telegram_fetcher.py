import logging
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import User

from .config import (
    TELEGRAM_API_ID,
    TELEGRAM_API_HASH,
    TELEGRAM_STRING_SESSION,
    TELEGRAM_CHAT_ID,
    TIMEZONE
)

logger = logging.getLogger("telegram_fetcher")

def resolve_chat_id(target):
    try:
        return int(target)
    except ValueError:
        return target

async def fetch_messages_since(hours_back: float = 8.0) -> list:
    """
    Connects to Telegram via MTProto with StringSession and retrieves all text messages
    posted within the last `hours_back` hours. Converts all timestamps to target timezone.
    """
    local_tz = ZoneInfo(TIMEZONE)
    cutoff_utc = datetime.now(timezone.utc) - timedelta(hours=hours_back)
    chat_target = resolve_chat_id(TELEGRAM_CHAT_ID)

    logger.info(f"Connecting to Telegram MTProto... Target chat: {chat_target}")
    client = TelegramClient(StringSession(TELEGRAM_STRING_SESSION), TELEGRAM_API_ID, TELEGRAM_API_HASH)
    
    extracted_messages = []
    
    await client.connect()
    if not await client.is_user_authorized():
        await client.disconnect()
        raise PermissionError("Telegram StringSession is invalid or expired. Re-run session generator.")

    try:
        chat = await client.get_entity(chat_target)
        chat_title = getattr(chat, "title", str(chat_target))
        logger.info(f"Successfully connected to '{chat_title}'. Fetching messages since {cutoff_utc.isoformat()}...")

        async for message in client.iter_messages(chat, limit=500):
            if not message.date or message.date < cutoff_utc:
                break

            text = message.text or message.message or ""
            if not text.strip():
                continue

            sender = await message.get_sender()
            sender_name = "Anónimo"
            if isinstance(sender, User):
                sender_name = sender.first_name or sender.username or "Usuario"
                if sender.last_name:
                    sender_name += f" {sender.last_name}"

            # Convert UTC date to configured timezone (Europe/Madrid default)
            date_local = message.date.astimezone(local_tz).strftime("%H:%M")

            extracted_messages.append({
                "id": message.id,
                "date_utc": message.date.isoformat(),
                "date_local": date_local,
                "sender_name": sender_name,
                "text": text.strip()
            })

    finally:
        await client.disconnect()

    # Sort chronologically (oldest first)
    extracted_messages.reverse()
    logger.info(f"Retrieved {len(extracted_messages)} messages from '{chat_title}'.")
    return extracted_messages
