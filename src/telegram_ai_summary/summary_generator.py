import json
import logging
import time
import urllib.request
import urllib.error
from .config import GEMINI_API_KEY, COMMUNITY_NAME

logger = logging.getLogger("summary_generator")

def get_system_instruction(community_name: str) -> str:
    return f"""
You are the official humorous, witty chronicler and digest writer for the Telegram community '{community_name}'.
Your task is to review recent chat messages (with sender, local time, and text) and generate a structured JSON summary digest for an infographic card.

STYLE & TONE GUIDELINES:
1. TONE: Funny, witty, sharp, lighthearted, and slightly sarcastic. Tease users lovingly about their habits, obsessions, early wake-up times, impulse purchases, gameplay excuses, or heated debates.
2. EMOJIS: Use expressive and diverse emojis both in section headers and in entry contents.
3. CLEAR SECTIONS: Group the conversations into 3 to 5 clever, thematic sections.
4. FORMATTING: You can use safe HTML tags in 'content' such as <strong> to highlight game titles, dates, or prices, and <em> for quotes.
5. BADGE COLORS: For each user entry, assign one badge color from: 'blue', 'purple', 'orange', 'green', 'red', 'yellow'.
6. TIMESTAMPS: The provided timestamps are already in the group's local timezone. Mention exact times when funny or relevant.

YOU MUST RETURN ONLY A STRICT VALID JSON OBJECT MATCHING THIS SCHEMA:
{{
  "title": "CATCHY ALL-CAPS HUMOROUS HEADLINE",
  "subtitle": "Witty subheadline tailored to the current time slot (e.g. overnight recap for morning, morning highlights for midday, afternoon wrap-up for evening)",
  "pills": [
    "📅 Date",
    "💬 {community_name}",
    "🕒 Time Slot"
  ],
  "sections": [
    {{
      "icon": "🎮",
      "title": "Section Title",
      "tagline": "Witty subtitle or tagline for the section",
      "entries": [
        {{
          "user": "Username",
          "badge_color": "blue",
          "content": "Humorous summary of what this person said or did..."
        }}
      ]
    }}
  ]
}}
"""

SUMMARY_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "title": {"type": "STRING"},
        "subtitle": {"type": "STRING"},
        "pills": {"type": "ARRAY", "items": {"type": "STRING"}},
        "sections": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "icon": {"type": "STRING"},
                    "title": {"type": "STRING"},
                    "tagline": {"type": "STRING"},
                    "entries": {
                        "type": "ARRAY",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "user": {"type": "STRING"},
                                "badge_color": {"type": "STRING"},
                                "content": {"type": "STRING"}
                            },
                            "required": ["user", "content"]
                        }
                    }
                },
                "required": ["title", "entries"]
            }
        }
    },
    "required": ["title", "subtitle", "sections"]
}

def normalize_summary_data(summary_json, current_slot: str = "") -> dict:
    """
    Ensures the summary data object is strictly a valid dictionary matching
    the required template schema, resilient to any variations returned by LLMs
    (direct object, wrapped list, or direct list of sections).
    """
    default_sub = "Humorous daily digest of recent community activity and highlights"
    s_lower = (current_slot or "").lower()
    if "full" in s_lower or "24h" in s_lower or "completo" in s_lower:
        default_sub = "The definitive full-day community debrief (00:00 - 23:59)"
    elif "morning" in s_lower or "07:00" in s_lower or "matinal" in s_lower:
        default_sub = "Overnight chronicles while normal people were asleep"
    elif "midday" in s_lower or "14:30" in s_lower or "mediodía" in s_lower:
        default_sub = "Morning highlights and pre-lunch banter"
    elif "evening" in s_lower or "22:00" in s_lower or "nocturna" in s_lower:
        default_sub = "Afternoon chronicles and prime-time gaming sessions"

    if isinstance(summary_json, list):
        if len(summary_json) == 1 and isinstance(summary_json[0], dict):
            summary_json = summary_json[0]
        elif len(summary_json) > 1 and all(isinstance(item, dict) for item in summary_json):
            root_candidate = next((item for item in summary_json if "sections" in item and isinstance(item["sections"], list)), None)
            if root_candidate:
                summary_json = root_candidate
            else:
                summary_json = {
                    "title": f"DIGEST: {COMMUNITY_NAME.upper()}",
                    "subtitle": default_sub,
                    "pills": [f"💬 {COMMUNITY_NAME}", f"🕒 {current_slot or 'Local'}"],
                    "sections": summary_json
                }
        elif len(summary_json) > 0 and isinstance(summary_json[0], dict):
            summary_json = summary_json[0]
        else:
            summary_json = {}

    if not isinstance(summary_json, dict):
        summary_json = {}

    if not summary_json.get("title") or not isinstance(summary_json.get("title"), str):
        summary_json["title"] = f"DIGEST: {COMMUNITY_NAME.upper()}"

    if not summary_json.get("subtitle") or not isinstance(summary_json.get("subtitle"), str):
        summary_json["subtitle"] = default_sub

    if not isinstance(summary_json.get("pills"), list):
        summary_json["pills"] = [f"💬 {COMMUNITY_NAME}", f"🕒 {current_slot or 'Local'}"]

    raw_sections = summary_json.get("sections")
    clean_sections = []
    if isinstance(raw_sections, list):
        for sec in raw_sections:
            if isinstance(sec, dict):
                entries = sec.get("entries")
                clean_entries = []
                if isinstance(entries, list):
                    for e in entries:
                        if isinstance(e, dict):
                            clean_entries.append({
                                "user": str(e.get("user", "Member")),
                                "badge_color": str(e.get("badge_color", "blue")),
                                "content": str(e.get("content", ""))
                            })
                        elif isinstance(e, str):
                            clean_entries.append({
                                "user": "Member",
                                "badge_color": "blue",
                                "content": e
                            })
                clean_sections.append({
                    "icon": str(sec.get("icon", "🎮")),
                    "title": str(sec.get("title", "Highlights")),
                    "tagline": str(sec.get("tagline", "")),
                    "entries": clean_entries
                })
    summary_json["sections"] = clean_sections
    return summary_json

def generate_summary(messages_data: list, current_slot: str = "") -> dict:
    if not messages_data:
        s_lower = (current_slot or "").lower()
        if "morning" in s_lower or "07:00" in s_lower or "matinal" in s_lower:
            slot_sub = "Morning edition: calm night with minimal chat activity"
        elif "midday" in s_lower or "14:30" in s_lower or "mediodía" in s_lower:
            slot_sub = "Midday edition: everyone focused on work/studies"
        else:
            slot_sub = "Evening edition: peace and quiet across the community"

        return {
            "title": f"BOLETÍN TRANQUILO: {COMMUNITY_NAME.upper()}",
            "subtitle": slot_sub,
            "pills": [f"💬 {COMMUNITY_NAME}", f"🕒 {current_slot or 'Current slot'}", "💤 Actividad mínima"],
            "sections": [
                {
                    "icon": "🕹️",
                    "title": "Silencio en el servidor",
                    "tagline": "O están viciando concentrados o currando duro",
                    "entries": [
                        {
                            "user": "Sistema",
                            "badge_color": "blue",
                            "content": f"No se registraron mensajes destacables en esta franja ({current_slot or 'reciente'}). ¡Todos al día con sus quehaceres!"
                        }
                    ]
                }
            ]
        }

    # Format chat corpus for prompt
    formatted_chat = []
    for m in messages_data:
        formatted_chat.append(f"[{m.get('date_local', '00:00')}] {m['sender_name']}: {m['text']}")
    chat_corpus = "\n".join(formatted_chat)

    prompt = f"""
Digest slot: {current_slot or 'Recent Activity Digest'}
Community: {COMMUNITY_NAME}

Chat messages in chronological order:
--- START OF MESSAGES ---
{chat_corpus}
--- END OF MESSAGES ---

Generate the structured JSON digest following all style and schema rules.
"""

    candidate_models = [
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite",
        "gemini-3-flash-preview",
        "gemini-flash-lite-latest"
    ]
    last_error = None

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
        "systemInstruction": {
            "parts": [
                {"text": get_system_instruction(COMMUNITY_NAME)}
            ]
        },
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": SUMMARY_RESPONSE_SCHEMA,
            "temperature": 0.7
        }
    }

    for model_name in candidate_models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        max_retries = 2
        for attempt in range(max_retries + 1):
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            try:
                with urllib.request.urlopen(req, timeout=40) as response:
                    res_data = json.loads(response.read().decode("utf-8"))
                    raw_text = res_data["candidates"][0]["content"]["parts"][0]["text"]
                    summary_json = json.loads(raw_text)
                    clean_summary = normalize_summary_data(summary_json, current_slot=current_slot)
                    logger.info(f"Summary successfully generated via Gemini API ({model_name}).")
                    return clean_summary
            except urllib.error.HTTPError as e:
                err_msg = e.read().decode("utf-8")
                last_error = f"{e.code} - {err_msg}"
                if e.code in (429, 500, 503, 504) and attempt < max_retries:
                    backoff = (attempt + 1) * 3
                    logger.warning(
                        f"Transient HTTP {e.code} on {model_name}. Retrying in {backoff}s (attempt {attempt + 1}/{max_retries})..."
                    )
                    time.sleep(backoff)
                    continue
                else:
                    logger.warning(f"HTTP {e.code} on model {model_name}: {err_msg[:120]}. Trying next candidate...")
                    break
            except Exception as e:
                last_error = str(e)
                if attempt < max_retries:
                    backoff = (attempt + 1) * 2
                    logger.warning(f"Error calling {model_name}: {e}. Retrying in {backoff}s...")
                    time.sleep(backoff)
                    continue
                else:
                    logger.warning(f"Error calling {model_name}: {e}. Trying next candidate...")
                    break

    raise RuntimeError(f"All Gemini candidate models failed: {last_error}")
