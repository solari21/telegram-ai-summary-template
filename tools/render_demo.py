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

# Ensure parent directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.card_renderer import render_summary_card

MOCK_SUMMARY = {
    "title": "EL GRAN DEBATE DEL BACKLOG Y COMPRAS COMPULSIVAS",
    "subtitle": "Crónica Gamer • 12 de Octubre de 2026 • Edición Nocturna",
    "pills": [
        "🎮 Pixel & Coffee Gaming",
        "🕒 22:00 CET",
        "🔥 Nivel de Hype: 98%"
    ],
    "sections": [
        {
            "icon": "🕹️",
            "title": "La Ruina de las Ofertas de Medianoche",
            "tagline": "Comprando juegos a 4.99€ que jamás van a instalar",
            "entries": [
                {
                    "user": "PixelKnight",
                    "badge_color": "blue",
                    "content": "Abre el hilo a las 15:30 con un dramático <em>'no me voy a comprar nada este mes'</em> y a las 20:15 anuncia que se ha pillado tres indies en oferta porque <strong>'estaban regalados'</strong>."
                },
                {
                    "user": "CyberSamurai",
                    "badge_color": "purple",
                    "content": "Confirma que su backlog supera ya los <strong>240 títulos pendientes</strong>, pero insiste en que el nuevo RPG espacial <em>'se lo pasa este fin de semana sin falta'</em>. Nadie le cree."
                }
            ]
        },
        {
            "icon": "☕",
            "title": "El Club de los Madrugadores Insomnes",
            "tagline": "Mensajes a horas intempestivas que desafían la biología humana",
            "entries": [
                {
                    "user": "RetroGamer88",
                    "badge_color": "orange",
                    "content": "A las <strong>06:12 de la mañana</strong> saluda con foto de su café y una partida de Game Boy Advance en la cama. Los demás aún estaban en fase REM profunda."
                },
                {
                    "user": "ValkyrieQueen",
                    "badge_color": "green",
                    "content": "Se queja de que <em>'los servidores de emparejamiento están muertos a las 7 AM'</em>. Quizá porque la gente normal a esa hora va a currar."
                }
            ]
        },
        {
            "icon": "💥",
            "title": "La Guerra de Resoluciones y Tasa de Refresco",
            "tagline": "30 FPS vs 144 FPS: La discusión milenaria que nunca muere",
            "entries": [
                {
                    "user": "FPS_Enthusiast",
                    "badge_color": "red",
                    "content": "Afirma con total solemnidad que <em>'a 59 FPS sus ojos sangran'</em>. Procedió a compartir gráficos de frametime durante 45 minutos seguidos."
                },
                {
                    "user": "CozyGamer",
                    "badge_color": "yellow",
                    "content": "Cierra el debate jugando plácidamente a <strong>Stardew Valley en una Switch</strong> a 30 FPS con una taza de té, inmune al caos técnico."
                }
            ]
        }
    ]
}

async def main():
    assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
    os.makedirs(assets_dir, exist_ok=True)
    output_path = os.path.join(assets_dir, "demo_summary.png")
    
    print(f"Rendering demo summary card to: {output_path}...")
    await render_summary_card(MOCK_SUMMARY, output_path=output_path)
    print("✅ Demo card rendered successfully!")

if __name__ == "__main__":
    asyncio.run(main())
