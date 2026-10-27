# 🚀 Telegram AI Daily Summary Bot & Generador de Infografías

<p align="left">
  <a href="README.md"><img src="https://img.shields.io/badge/Espa%C3%B1ol-Activo-orange?style=flat&logo=readme&logoColor=white" height="20" alt="Versión en Español" /></a>
  &nbsp;
  <a href="README_EN.md"><img src="https://img.shields.io/badge/English-Switch-blue?style=flat&logo=googletranslate&logoColor=white" height="20" alt="Switch to English" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg?style=flat&logo=python&logoColor=white" height="20" alt="Python Version" />
  &nbsp;
  <a href="https://github.com/solari21/telegram-ai-summary-template/releases/tag/v0.4.0"><img src="https://img.shields.io/badge/release-v0.4.0-blue.svg?style=flat&logo=github" height="20" alt="Release v0.4.0" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/REA%20MCP-Web%20Stability-success?style=flat&logo=shield&logoColor=white" height="20" alt="REA MCP Web Stability" />
  &nbsp;
  <img src="https://img.shields.io/badge/automation-GitHub_Actions-2088FF.svg?style=flat&logo=github-actions&logoColor=white" height="20" alt="GitHub Actions" />
  &nbsp;
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=flat" height="20" alt="License MIT" />
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
- 🎨 **Estabilidad Web & Renderizado Nítido (REA MCP Integration)**: Plantilla personalizada Jinja2 HTML5/CSS3 renderizada con Playwright Chromium con factor de escala 2x (Retina). Integra el motor de estabilización de ejecución web de **REA MCP** (`document.fonts.ready` y doble frame de composición con `requestAnimationFrame`), eliminando layout shifts y fuentes de fallback pixeladas.
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
* **07:00 Local** (06:02 UTC Invierno CET / 05:02 UTC Verano CEST): Ventana fija **22:00 (ayer) a 07:00 (hoy)**.
* **14:30 Local** (13:32 UTC Invierno CET / 12:32 UTC Verano CEST): Ventana fija **07:00 a 14:30 (hoy)**.
* **22:00 Local** (21:02 UTC Invierno CET / 20:02 UTC Verano CEST): Ventana fija **14:30 a 22:00 (hoy)**.

### 2. Resumen Diario Completo 24 Horas (`full_day_summary.yml`)
* Se dispara cada noche a las **23:58 Madrid** (21:58 UTC).
* Recopila **toda la jornada (00:00:00 a 23:59:59)** y genera el parte completo del día.

### 3. Disparador Manual a la Carta (`manual_summary.yml`)
* Permite generar un resumen interactivo a petición desde la pestaña Actions de GitHub eligiendo el número de horas hacia atrás y un título opcional.

---

## ⚡ Resiliencia de Franjas y Rendimiento CI/CD (v0.4.0)

Esta actualización incorpora mejoras críticas de estabilidad y rendimiento probadas en entornos de alta producción:

* 🎯 **Navegación MTProto Directa con `offset_date`**: Telethon salta directamente al instante final de cada franja horaria sin descargar los mensajes posteriores del grupo. Esto elimina la inanición por límite de iteración (`limit=400`) y garantiza que los resúmenes programados o manuales se procesen en ~1 segundo.
* 🚀 **Aceleración CI/CD con Caché de Playwright**: Se integra `actions/cache@v4` sobre `~/.cache/ms-playwright` y un `timeout-minutes: 20`. El tiempo de preparación del navegador Chromium en GitHub Actions se reduce de ~8 minutos a escasos segundos.
* 🕒 **Conmutación Horaria CET/CEST**: Expresiones cron ajustadas para invierno (CET UTC+1: `06:02`, `13:32`, `21:02` UTC) y parser adaptado para reconocer dinámicamente franjas horarias tanto de verano como de invierno.
* ⏱️ **Clamping Dinámico de Ventana**: Si un resumen se dispara interactivamente antes del fin de franja, el límite superior se ajusta a la hora actual (`now`), permitiendo pruebas inmediatas a la carta.
* 🛡️ **Garantía de Entrega ("Franja Tranquila")**: En caso de ausencia total de mensajes en el grupo durante un intervalo, genera y entrega la tarjeta oficial de «Franja Tranquila / Sin Novedad» en lugar de abortar silenciosamente.

---

## 🚀 Despliegue Rápido en 3 Pasos

### 1. Haz clic en "Use this template"
Crea tu propio repositorio privado o público a partir de esta plantilla en GitHub.

### 2. Configura los Secretos del Repositorio
En tu repositorio de GitHub, ve a **Settings > Secrets and variables > Actions** y añade:
- `TELEGRAM_API_ID`: Tu API ID de Telegram (desde https://my.telegram.org).
- `TELEGRAM_API_HASH`: Tu API Hash de Telegram.
- `TELEGRAM_STRING_SESSION`: La sesión de Telethon en formato string (genérala con `python tools/generate_string_session.py`).
- `TELEGRAM_CHAT_ID`: El ID del grupo de Telegram a resumir (ej. `-1001234567890`).
- `TELEGRAM_SEND_TO`: `me` (para Mensajes Guardados) o el ID numérico del canal/grupo receptor.
- `GEMINI_API_KEY`: Tu clave de API de Google AI Studio (gratuita).

### 3. ¡Listo!
Tus workflows comenzarán a ejecutarse en los horarios programados o cuando los dispares manualmente.

---

## 📦 Uso como Paquete CLI de Python

También puedes instalar este proyecto como un paquete CLI estándar:

```bash
pip install .
telegram-ai-summary --demo  # Genera una infografía de demostración sin necesidad de credenciales
```

---

## 🛡️ Créditos y Reconocimientos

- **REA MCP (`rea-agents@6.7.0`)**: Capacidades de análisis de ejecución web, auditoría estática y estabilización de fuentes.
- **Google Gemini**: Modelos multimodales para síntesis conversacional y análisis de tono humorístico.
- **Telethon**: Cliente MTProto asíncrono para Telegram.
- **Playwright**: Motor de renderizado Chromium de alta resolución.

---

## 📋 Gestión del Proyecto y Hoja de Ruta

- 📌 **Tablero Kanban GitHub Projects V2**: [Telegram AI Digest Roadmap](https://github.com/users/solari21/projects/1)
- 📝 **Checklist de hitos**: [TODO.md](TODO.md)

---

## 📄 Licencia

Publicado bajo la licencia [MIT](LICENSE).
