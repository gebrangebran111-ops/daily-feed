import json
import logging
import os
import time
from datetime import datetime, timezone
from urllib import error, request

logger = logging.getLogger("daily_feed.openai")

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


def _extract_json_object(content):
    start = content.find("{")
    end = content.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise ValueError("OpenAI response did not include valid JSON.")
    return json.loads(content[start: end + 1])


def generate_ai_recommendations():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY env variable is missing — cannot call OpenAI")
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    prompt = f"""
You are generating two sections for a daily email digest for a user in Lebanon.
Generate content for date: {today}. Make today's picks feel different from yesterday:
- vary music genre/era/tempo
- vary adventure terrain and vibe

Return ONLY valid JSON (no markdown) with this exact schema:
{{
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
- Song should be popular and playable on guitar with realistic chord progression.
- Adventure must be in Lebanon.
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

    retries = 3
    backoff_seconds = 5
    body = None

    for attempt in range(retries):
        logger.info("POST %s (attempt %d/%d)", OPENAI_URL, attempt + 1, retries)
        req = request.Request(
            OPENAI_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=60) as response:
                logger.info("OpenAI response status: %s", response.status)
                body = json.loads(response.read().decode("utf-8"))
            break
        except error.HTTPError as exc:
            logger.error("OpenAI HTTP error %s: %s", exc.code, exc.reason)
            if exc.code == 429 and attempt < retries - 1:
                retry_after = exc.headers.get("Retry-After")
                sleep_for = int(retry_after) if retry_after and retry_after.isdigit() else backoff_seconds
                logger.warning("Rate limited (429). Retrying in %ds...", sleep_for)
                time.sleep(sleep_for)
                backoff_seconds *= 2
                continue
            raise
        except error.URLError as exc:
            logger.error("OpenAI URL error: %s", exc.reason)
            raise
        except Exception as exc:
            logger.error("Unexpected error calling OpenAI: %s", exc)
            raise

    if body is None:
        raise ValueError("OpenAI call failed after all retries.")

    content = body["choices"][0]["message"]["content"]
    logger.info("OpenAI raw response length: %d chars", len(content))

    parsed = _extract_json_object(content)

    if not parsed.get("song") or not parsed.get("adventure"):
        logger.error("OpenAI response missing required fields. Got: %s", list(parsed.keys()))
        raise ValueError("OpenAI response missing required fields.")

    logger.info("OpenAI response parsed successfully")
    return parsed
