#!/usr/bin/env python3
"""
Telegram StringSession Generator
---------------------------------
Run this script once locally to generate a TELEGRAM_STRING_SESSION for your account.
This session string can be safely stored in GitHub Secrets or .env without needing
a session file on disk.

Usage:
    python tools/generate_string_session.py
"""

import sys
import asyncio
from telethon import TelegramClient
from telethon.sessions import StringSession

async def main():
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

if __name__ == "__main__":
    asyncio.run(main())
