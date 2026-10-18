# 🚀 Telegram AI Daily Summary Bot & Generador de Infografías

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Release](https://img.shields.io/badge/release-v0.2.0-blue.svg?logo=github)](https://github.com/solari21/telegram-ai-summary-template/releases/tag/v0.2.0)
[![GitHub Actions](https://img.shields.io/badge/automation-GitHub_Actions-2088FF.svg?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Google Gemini API](https://img.shields.io/badge/AI-Gemini_3.8_Flash_%26_Cascade-8E75B2.svg?logo=google&logoColor=white)](https://aistudio.google.com/)
[![Telethon](https://img.shields.io/badge/telegram-Telethon_MTProto-2CA5E0.svg?logo=telegram&logoColor=white)](https://docs.telethon.dev/)
[![Playwright](https://img.shields.io/badge/renderer-Playwright_Chromium-45ba4b.svg?logo=playwright&logoColor=white)](https://playwright.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<p align="center">
  <a href="README.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-Activo-orange?style=for-the-badge&logo=readme&logoColor=white" alt="Versión en Español" /></a>
  &nbsp;&nbsp;
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-Switch-blue?style=for-the-badge&logo=googletranslate&logoColor=white" alt="Switch to English" /></a>
</p>

> **Transforma comunidades activas y grupos gamer de Telegram en infografías visualmente espectaculares con resúmenes cómicos generados por IA. Disponible tanto como Plantilla Serverless automatizada como Paquete CLI de Python instalable.**

---

## 📸 Vista Previa de la Infografía

Ejemplo real de la infografía en alta definición generada automáticamente por este bot:

<p align="center">
  <img src="assets/demo_summary.png" alt="Demo Infografía Telegram AI Daily Summary" width="700">
</p>




---

## ✨ Características Principales

- ⚡ **100% Serverless y Gratuito**: Se ejecuta mediante crons programados en GitHub Actions. Cero VPS, cero costes de hosting y cero servidores encendidos 24/7.
- 📅 **Triple Modalidad de Ejecución**:
  1. **Resúmenes por Franjas**: Matinal (07:00), Mediodía (14:30) y Nocturna (22:00) con subtítulos dinámicos y ventanas fijas de inspección.
  2. **Resumen Diario Completo**: Recopilación a medianoche que cubre las 24 horas del día (00:00 a 23:59).
  3. **Lanzamiento Manual a la Carta**: Ejecuta en cualquier momento desde GitHub Actions o CLI con horas relativas personalizadas (ej. 2, 4, 8, 12, 24, 48) y títulos custom.
- 🧠 **Cascada de 5 Modelos de IA con Reintentos Exponenciales**: Diseñado para el vanguardista **Google Gemini 3.8 Flash**, con reintentos automáticos (backoff de 3s / 6s) y conmutación tolerante a fallos hacia **3.5 Flash**, **3.5 Flash Lite**, **2.0 Flash** y **2.0 Flash Lite** ante picos de servidores de Google (503 / 500 / 429).
- 🎨 **Infografías Dark-Mode en Calidad Retina**: Plantilla personalizada Jinja2 HTML5/CSS3 renderizada con Chromium Headless mediante Playwright con factor de escala 2x para tipografías ultra nítidas y badges vibrantes.
- 🔐 **Arquitectura Cero Fugas**: Utiliza `StringSession` de Telethon y secretos cifrados de GitHub Actions. Sin archivos SQLite de sesión en disco.
- 🕒 **Detección Inteligente de Zonas Horarias**: Calcula automáticamente las ventanas de inspección y convierte los timestamps a tu zona horaria local (ej. `Europe/Madrid`).
- 🛠️ **Plantilla Abierta y Reutilizable**: Ningún token privado, ID de chat o mensaje está hardcodeado. Lista para clonar, configurar y desplegar en menos de 5 minutos.

---

## 🏛️ Arquitectura del Sistema y Flujo de Trabajo

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/architecture-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="assets/architecture-light.svg">
    <img alt="Arquitectura y Flujo Telegram AI Daily Summary" src="assets/architecture.svg" width="950">
  </picture>
</p>

---

## 📅 Modos de Automatización en GitHub Actions

La plantilla incluye **3 workflows listos para producción**:

### 1. Resumen por Franjas (`daily_summary.yml`)
Se ejecuta automáticamente 3 veces al día en minutos alternos (`:02` y `:32`) para evitar demoras en las colas de GitHub Actions en horas en punto:
* **07:00 Local** (05:02 UTC en horario de verano): Ventana fija **22:00 (ayer) a 07:00 (hoy)**.
* **14:30 Local** (12:32 UTC en horario de verano): Ventana fija **07:00 a 14:30 (hoy)**.
* **22:00 Local** (20:02 UTC en horario de verano): Ventana fija **14:30 a 22:00 (hoy)**.

### 2. Resumen Diario Completo de 24 Horas (`full_day_summary.yml`)
* Se ejecuta a las **23:58 Local** cubriendo **00:00 a 23:59**.
* *Resiliencia de medianoche*: Si el runner sufre retraso y arranca de madrugada (00:00 a 05:59), analiza automáticamente el día completo de ayer.

### 3. Resumen Manual a la Carta (`manual_summary.yml`)
Permite lanzar un resumen en cualquier instante especificando el número de horas hacia atrás y un título opcional para la tarjeta.

---

## 🚀 Guía de Puesta en Marcha Rápida (5 Minutos)

### Paso 1: Usar esta plantilla
Haz clic en el botón verde **Use this template** ➔ **Create a new repository** en GitHub.

### Paso 2: Obtener Credenciales
1. **Telegram API ID & Hash**: Accede a [my.telegram.org](https://my.telegram.org) ➔ *API development tools*.
2. **Telegram StringSession**:
   ```bash
   pip install telethon
   python tools/generate_string_session.py
   ```
3. **Google Gemini API Key**: Consigue una clave gratuita en [Google AI Studio](https://aistudio.google.com/).

### Paso 3: Configurar Secretos en GitHub
Ve a tu repositorio ➔ **Settings** ➔ **Secrets and variables** ➔ **Actions** y añade:
- `TELEGRAM_API_ID`: Tu API ID de Telegram (entero).
- `TELEGRAM_API_HASH`: Tu API Hash de Telegram (cadena).
- `TELEGRAM_STRING_SESSION`: La cadena generada por el script.
- `TELEGRAM_CHAT_ID`: ID numérico del grupo (los supergrupos empiezan por `-100...`).
- `GEMINI_API_KEY`: Tu clave de Gemini API.
- *(Opcional)* `TELEGRAM_SEND_TO`: Destino de la infografía (`me` para tus Mensajes Guardados o ID de canal).

---

## 💻 Instalación como Paquete CLI de Python

```bash
# Clonar e instalar en modo editable:
git clone https://github.com/solari21/telegram-ai-summary-template.git
cd telegram-ai-summary-template
pip install -e .
playwright install chromium

# Ejecutar el resumen:
telegram-ai-summary run --slot morning

# O generar sesión de Telegram:
telegram-ai-summary session

# O generar una infografía demo sin APIs:
telegram-ai-summary demo
```

---

## 📁 Estructura del Repositorio

```
telegram-ai-summary-template/
├── .github/
│   └── workflows/
│       ├── daily_summary.yml       # Resumen por franjas con autodetección
│       ├── full_day_summary.yml    # Resumen diario completo (24 horas)
│       ├── manual_summary.yml      # Disparador manual a la carta
│       └── publish_package.yml     # Workflow de Release y empaquetado PyPI
├── assets/
│   ├── architecture-dark.png       # Arquitectura Retina @2x (dark)
│   ├── architecture-dark.svg       # Vectorial SVG standalone (dark)
│   ├── architecture-light.png      # Arquitectura Retina @2x (light)
│   ├── architecture-light.svg      # Vectorial SVG standalone (light)
│   ├── architecture.svg            # Diagrama universal
│   └── demo_summary.png            # Infografía de muestra
├── src/telegram_ai_summary/
│   ├── __init__.py
│   ├── card_renderer.py            # Renderizado HTML/CSS a PNG Retina
│   ├── cli.py                      # CLI modular (run, session, demo)
│   ├── config.py                   # Carga de variables de entorno
│   ├── mock_data.py                # Dataset simulado para demo
│   ├── summary_generator.py        # Cascada de IA con Google Gemini
│   ├── telegram_fetcher.py         # Extracción de mensajes MTProto
│   ├── telegram_sender.py          # Despacho de infografía
│   └── templates/
│       └── card_template.html      # Plantilla Jinja2 dark mode
├── tools/
│   ├── generate_string_session.py  # Generador de StringSession
│   ├── render_demo.py              # Renderizador de demo
│   ├── setup_windows_scheduler.ps1 # Programador para Windows
│   └── trigger_summary.py          # Disparador REST API
├── pyproject.toml                  # Configuración de paquete Python
├── requirements.txt                # Dependencias
├── TODO.md                         # Roadmap
├── README.md                       # Documentación en inglés
└── README_ES.md                    # Documentación en español
```

---

## 📋 Gestión del Proyecto y Hoja de Ruta

- 📌 **Tablero Kanban GitHub Projects V2**: [Telegram AI Digest Roadmap](https://github.com/users/solari21/projects/1)
- 📝 **Checklist de hitos**: [TODO.md](TODO.md)

---

## 📄 Licencia

Publicado bajo la licencia [MIT](LICENSE).
