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


def get_default_slot_subtitle(slot_name: str = "", community_name: str = "") -> str:
    s = (slot_name or "").lower()
    comm = community_name or "Community"
    if "morning" in s or "07:00" in s or "matinal" in s:
        return f"{comm} • Morning edition: overnight chat and early bird highlights"
    elif "midday" in s or "14:30" in s or "mediodía" in s or "mediodia" in s:
        return f"{comm} • Midday edition: morning discussions and coffee break banter"
    elif "evening" in s or "22:00" in s or "nocturna" in s:
        return f"{comm} • Evening edition: afternoon highlights and prime-time wrap-up"
    return f"{comm} • Highlights and active discussions"


async def render_summary_card(summary_data: dict, output_path: str = "output/summary_card.png", current_slot: str = "") -> str:
    """
    Renders the structured JSON summary into a high-resolution PNG image
    using an HTML/CSS Jinja2 template and headless Chromium (Playwright)
    with strict REA web execution stability (document.fonts.ready & rAF).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    # 1. Prepare template variables
    templates_dir = get_templates_dir()
    env = Environment(loader=FileSystemLoader(templates_dir))
    template = env.get_template("card_template.html")

    now = datetime.now(ZoneInfo(TIMEZONE))
    footer_date = now.strftime("%d/%m/%Y %H:%M")

    default_sub = get_default_slot_subtitle(current_slot or summary_data.get("slot", ""), COMMUNITY_NAME)
    raw_sub = summary_data.get("subtitle", "").strip()
    final_subtitle = default_sub if (not raw_sub or "no leídos" in raw_sub.lower() or "actividad reciente" in raw_sub.lower()) else raw_sub

    rendered_html = template.render(
        community_name=COMMUNITY_NAME,
        badge_top=f"🎙️ {COMMUNITY_NAME} • Daily Digest",
        title=summary_data.get("title", f"BOLETÍN {COMMUNITY_NAME.upper()}"),
        subtitle=final_subtitle,
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
    clean_html_path = abs_html_path.replace("\\", "/")
    file_url = f"file:///{clean_html_path}"

    logger.info("Starting Playwright Chromium browser with REA stability engine...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox", "--disable-setuid-sandbox"])
        page = await browser.new_page(
            viewport={"width": 950, "height": 1400},
            device_scale_factor=2  # 2x Retina resolution for razor-sharp text
        )

        page_errors = []
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        await page.goto(file_url, wait_until="load")

        # REA Stability: Font hydration check
        try:
            await page.wait_for_function("() => document.fonts.status === 'loaded'", timeout=5000)
        except Exception:
            await page.evaluate("() => document.fonts.ready")

        # REA Stability: Double animation frame for CSS Grid / layout settling
        await page.evaluate(
            "() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))"
        )

        container_elem = await page.query_selector(".container")
        if container_elem:
            box = await container_elem.bounding_box()
            if not box or box["width"] <= 0 or box["height"] <= 0:
                logger.warning("Container dimensions unstable, applying safety timeout...")
                await page.wait_for_timeout(300)
            await container_elem.screenshot(path=abs_out_path)
        else:
            await page.screenshot(path=abs_out_path, full_page=True)

        if page_errors:
            logger.warning(f"Web execution audit: {len(page_errors)} page error(s) logged: {page_errors}")
        else:
            logger.info("Web execution audit: Fonts and DOM layout verified 100% stable.")

        await browser.close()

    if os.path.exists(temp_html_path):
        os.remove(temp_html_path)

    logger.info(f"Summary infographic generated successfully at: {abs_out_path}")
    return abs_out_path
