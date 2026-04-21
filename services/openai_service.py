import json
import os
from datetime import datetime, timezone
from urllib import request


OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def _extract_json_object(content):
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("OpenAI response did not include valid JSON.")
    return json.loads(content[start : end + 1])


def generate_daily_content():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("Set OPENAI_API_KEY environment variable.")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    prompt = f"""
You are generating a daily email digest for a user in Lebanon.
Generate content for date: {today}.
Make it feel different from previous days in tone and choices.

Return ONLY valid JSON (no markdown) with this exact schema:
{{
  "quote": "string",
  "song": {{
    "title": "string",
    "artist": "string",
    "difficulty": "easy|medium|hard",
    "chords": "string"
  }},
  "adventure": {{
    "name": "string",
    "type": "Hiking|Camping|Hiking/Camping",
    "difficulty": "easy|medium|hard",
    "description": "string",
    "country": "Lebanon"
  }}
}}

Rules:
- Keep quote short and inspiring.
- Song should be popular and playable on guitar with realistic chord progression.
- Adventure must be in Lebanon.
- Avoid repeating the same artist/style as a typical previous day.
- Keep fields concise and clean for newsletter formatting.
""".strip()

    payload = {
        "model": "gpt-4o-mini",
        "temperature": 0.9,
        "messages": [
            {"role": "system", "content": "You produce structured JSON only."},
            {"role": "user", "content": prompt},
        ],
    }

    req = request.Request(
        OPENAI_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with request.urlopen(req, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))

    content = body["choices"][0]["message"]["content"]
    parsed = _extract_json_object(content)

    if not parsed.get("quote") or not parsed.get("song") or not parsed.get("adventure"):
        raise ValueError("OpenAI response missing required fields.")
    return parsed
