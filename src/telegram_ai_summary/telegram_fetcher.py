import logging
from datetime import datetime, timedelta, timezone
try:
    from zoneinfo import ZoneInfo
except ImportError:
    import pytz
    ZoneInfo = pytz.timezone
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

logger = logging.getLogger("telegram_ai_summary.fetcher")

def resolve_chat_id(target):
    try:
        return int(target)
    except ValueError:
        return target

async def fetch_messages_since(
    hours_back: float = 8.0,
    full_day: bool = False,
    start_time_local: datetime = None,
    end_time_local: datetime = None
) -> list:
    """
    Fetches Telegram chat messages within:
    1. A deterministic local time window (start_time_local and end_time_local),
    2. Today's full day (00:00:00 to 23:59:59 local time), or
    3. The relative last `hours_back` hours.
    Uses offset_date to jump directly to the target window without burning quota on newer messages.
    Converts all timestamps to target timezone.
    """
    local_tz = ZoneInfo(TIMEZONE)
    now_local = datetime.now(local_tz)
    now_utc = datetime.now(timezone.utc)

    offset_date = None
    target_date = None

    if start_time_local and end_time_local:
        cutoff_utc = start_time_local.astimezone(timezone.utc)
        end_utc = end_time_local.astimezone(timezone.utc)
        if end_utc <= now_utc:
            offset_date = end_utc
        effective_limit = 1000
        logger.info(
            f"EXACT WINDOW MODE active. Fetching between {start_time_local.strftime('%Y-%m-%d %H:%M:%S')} "
            f"and {end_time_local.strftime('%Y-%m-%d %H:%M:%S')} {TIMEZONE} (offset_date={offset_date})..."
        )
    elif full_day:
        if now_local.hour < 6:
            target_date = (now_local - timedelta(days=1)).date()
            start_of_day_local = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=local_tz)
            end_of_day_local = datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59, 999999, tzinfo=local_tz)
            cutoff_utc = start_of_day_local.astimezone(timezone.utc)
            end_utc = end_of_day_local.astimezone(timezone.utc)
            if end_utc <= now_utc:
                offset_date = end_utc
        else:
            target_date = now_local.date()
            start_of_day_local = datetime(target_date.year, target_date.month, target_date.day, 0, 0, 0, tzinfo=local_tz)
            end_of_day_local = now_local
            cutoff_utc = start_of_day_local.astimezone(timezone.utc)
            end_utc = None
            offset_date = None

        effective_limit = 1500
        logger.info(f"FULL-DAY MODE active. Fetching target date {target_date.strftime('%Y-%m-%d')} ({start_of_day_local.strftime('%H:%M:%S')} to {end_of_day_local.strftime('%H:%M:%S')} {TIMEZONE})...")
    else:
        cutoff_utc = now_utc - timedelta(hours=hours_back)
        effective_limit = 600
        end_utc = None
        target_date = None
        offset_date = None
        logger.info(f"SLOT/MANUAL MODE active. Fetching messages since {cutoff_utc.isoformat()} (last {hours_back} hours)...")

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
        logger.info(f"Successfully connected to '{chat_title}'. Fetching messages...")

        async for message in client.iter_messages(chat, offset_date=offset_date, limit=effective_limit):
            if not message.date:
                continue
            msg_date_utc = message.date if message.date.tzinfo else message.date.replace(tzinfo=timezone.utc)
            if end_utc and msg_date_utc > end_utc:
                continue
            if msg_date_utc < cutoff_utc:
                break

            text = message.text or message.message or ""
            if not text.strip():
                continue

            sender = await message.get_sender()
            sender_name = "Anonymous"
            if sender:
                if isinstance(sender, User):
                    names = [sender.first_name or "", sender.last_name or ""]
                    sender_name = " ".join(n for n in names if n).strip() or "User"
                else:
                    sender_name = getattr(sender, "title", "Channel/Group")

            msg_local = msg_date_utc.astimezone(local_tz)

            extracted_messages.append({
                "id": message.id,
                "sender_name": sender_name,
                "date_local": msg_local.strftime("%H:%M"),
                "date_utc": msg_date_utc.strftime("%Y-%m-%d %H:%M:%S"),
                "text": text.strip()
            })
    finally:
        await client.disconnect()

    extracted_messages.reverse()
    logger.info(f"Retrieved {len(extracted_messages)} messages.")
    return extracted_messages
