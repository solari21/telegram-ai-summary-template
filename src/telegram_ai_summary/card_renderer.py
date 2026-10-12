import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo
from jinja2 import Environment, FileSystemLoader
from playwright.async_api import async_playwright

from .config import TIMEZONE, COMMUNITY_NAME

logger = logging.getLogger("card_renderer")

def get_templates_dir() -> str:
    # 1. Package bundled templates directory
    pkg_templates = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
    if os.path.isdir(pkg_templates) and os.path.exists(os.path.join(pkg_templates, "card_template.html")):
        return pkg_templates

    # 2. Project root fallback
    root_templates = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "templates")
    if os.path.isdir(root_templates) and os.path.exists(os.path.join(root_templates, "card_template.html")):
        return root_templates

    return pkg_templates

async def render_summary_card(summary_data: dict, output_path: str = "output/summary_card.png") -> str:
    """
    Renders the structured JSON summary into a high-resolution PNG image
    using an HTML/CSS Jinja2 template and headless Chromium (Playwright).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Prepare template variables
    templates_dir = get_templates_dir()
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("card_template.html")

    now = datetime.now(ZoneInfo(TIMEZONE))
    footer_date = now.strftime("%d/%m/%Y %H:%M")

    rendered_html = template.render(
        community_name=COMMUNITY_NAME,
        badge_top=f"🎙️ {COMMUNITY_NAME} • Daily Digest",
        title=summary_data.get("title", f"BOLETÍN {COMMUNITY_NAME.upper()}"),
        subtitle=summary_data.get("subtitle", "Resumen de actividad reciente"),
        pills=summary_data.get("pills", [f"💬 {COMMUNITY_NAME}"]),
        sections=summary_data.get("sections", []),
        footer_date=footer_date
    )

    temp_html_path = output_path.replace(".png", ".html")
    with open(temp_html_path, "w", encoding="utf-8") as f:
        f.write(rendered_html)

    # 2. Render to PNG with Playwright async API
    abs_html_path = os.path.abspath(temp_html_path)
    abs_out_path = os.path.abspath(output_path)
    file_url = f"file:///{abs_html_path.replace('\\', '/')}"

    logger.info("Starting Playwright Chromium browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page(
            viewport={"width": 950, "height": 1400},
            device_scale_factor=2 # 2x Retina resolution for razor-sharp text
        )

        await page.goto(file_url, wait_until="networkidle")
        container_elem = await page.query_selector(".container")

        if container_elem:
            await container_elem.screenshot(path=abs_out_path)
        else:
            await page.screenshot(path=abs_out_path, full_page=True)

        await browser.close()

    # Clean up temporary HTML file
    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    logger.info(f"Summary infographic generated successfully at: {abs_out_path}")
    return abs_out_path
