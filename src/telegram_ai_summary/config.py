import os
from dotenv import load_dotenv

# Load .env file for local development if available
load_dotenv()

TELEGRAM_API_ID = int(os.environ.get("TELEGRAM_API_ID", 0))
TELEGRAM_API_HASH = os.environ.get("TELEGRAM_API_HASH", "").strip()
TELEGRAM_STRING_SESSION = os.environ.get("TELEGRAM_STRING_SESSION", "").strip()
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
TELEGRAM_SEND_TO = os.environ.get("TELEGRAM_SEND_TO", "me").strip()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "").strip()
TIMEZONE = os.environ.get("TIMEZONE", "Europe/Madrid")
HORAS_ATRAS = float(os.environ.get("HORAS_ATRAS", 8.0))
COMMUNITY_NAME = os.environ.get("COMMUNITY_NAME", "Comunidad Gamer").strip()

def validate_config():
    missing = []
    if not TELEGRAM_API_ID:
        missing.append("TELEGRAM_API_ID")
    if not TELEGRAM_API_HASH:
        missing.append("TELEGRAM_API_HASH")
    if not TELEGRAM_STRING_SESSION:
        missing.append("TELEGRAM_STRING_SESSION")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")
    if not GEMINI_API_KEY:
        missing.append("GEMINI_API_KEY")
    
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            "Please check your .env file or GitHub Secrets."
        )
