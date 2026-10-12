#!/usr/bin/env python3
"""
Demo Infographic Card Renderer
------------------------------
Generates a mock preview image for the repository README.md without needing
Telegram credentials or Gemini API calls.

Usage:
    python tools/render_demo.py
"""

import sys
import os
import asyncio

# Ensure parent and src directory are in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

from telegram_ai_summary.mock_data import MOCK_SUMMARY
from telegram_ai_summary.card_renderer import render_summary_card

async def main():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    output_path = os.path.join(assets_dir, "demo_summary.png")
    
    print(f"Rendering demo summary card to: {output_path}...")
    await render_summary_card(MOCK_SUMMARY, output_path=output_path)
    print("✅ Demo card rendered successfully!")

if __name__ == "__main__":
    asyncio.run(main())
