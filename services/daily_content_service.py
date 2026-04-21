import json
import logging
import os
from urllib import parse, request

from services.openai_service import generate_ai_recommendations


logger = logging.getLogger("daily_feed")


def _fetch_json(url, headers=None, timeout=20):
    req = request.Request(url, headers=headers or {})
    with request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def get_verse_of_the_day():
    logger.info("Fetching verse of the day")
    try:
        data = _fetch_json("https://beta.ourmanna.com/api/v1/get/?format=json")
        details = data["verse"]["details"]
        logger.info("Verse fetched successfully")
        return {
            "text": details["text"].strip(),
            "reference": details["reference"].strip(),
        }
    except Exception as exc:
        logger.exception("Verse fetch failed: %s", exc)
        return {
            "text": "For with God nothing shall be impossible.",
            "reference": "Luke 1:37",
        }


def _weather_label(weather_code):
    code_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Rime fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Rain",
        65: "Heavy rain",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
    }
    return code_map.get(weather_code, "Mixed weather")


def get_weather():
    logger.info("Fetching weather forecast")
    # Beirut coordinates
    lat, lon = 33.8938, 35.5018
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum"
        "&timezone=Asia%2FBeirut&forecast_days=2"
    )
    try:
        data = _fetch_json(url)
        daily = data["daily"]
        days = []
        for i in range(2):
            days.append(
                {
                    "date": daily["time"][i],
                    "condition": _weather_label(daily["weathercode"][i]),
                    "temp_max": round(daily["temperature_2m_max"][i]),
                    "temp_min": round(daily["temperature_2m_min"][i]),
                    "rain_mm": round(daily["precipitation_sum"][i], 1),
                }
            )
        logger.info("Weather fetched successfully")
        return {"city": "Beirut, Lebanon", "days": days}
    except Exception as exc:
        logger.exception("Weather fetch failed: %s", exc)
        return {
            "city": "Beirut, Lebanon",
            "days": [
                {
                    "date": "Today",
                    "condition": "Unavailable",
                    "temp_max": "-",
                    "temp_min": "-",
                    "rain_mm": "-",
                },
                {
                    "date": "Tomorrow",
                    "condition": "Unavailable",
                    "temp_max": "-",
                    "temp_min": "-",
                    "rain_mm": "-",
                },
            ],
        }


def get_international_news():
    logger.info("Fetching international news")
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        logger.error("NEWSAPI_KEY missing; news section will use fallback")
        return {
            "headlines": [
                {
                    "title": "International news unavailable (missing NEWSAPI_KEY).",
                    "source": "Setup needed",
                }
            ]
        }

    query = parse.urlencode(
        {
            "q": "(politics OR economy OR technology OR geopolitics OR diplomacy)",
            "language": "en",
            "sortBy": "popularity",
            "pageSize": 12,
        }
    )
    url = f"https://newsapi.org/v2/everything?{query}"
    try:
        data = _fetch_json(url, headers={"X-Api-Key": api_key})
        seen_titles = set()
        headlines = []
        for article in data.get("articles", []):
            title = (article.get("title") or "").strip()
            source = (article.get("source", {}).get("name") or "Unknown").strip()
            if not title or title in seen_titles:
                continue
            seen_titles.add(title)
            headlines.append({"title": title, "source": source})
            if len(headlines) == 3:
                break
        if not headlines:
            raise ValueError("No news headlines returned.")
        logger.info("News fetched successfully: %s headlines", len(headlines))
        return {"headlines": headlines}
    except Exception as exc:
        logger.exception("News fetch failed: %s", exc)
        return {
            "headlines": [
                {
                    "title": "Could not fetch international news right now.",
                    "source": "News API",
                }
            ]
        }


def get_fun_fact():
    logger.info("Fetching fun fact")
    try:
        data = _fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        logger.info("Fun fact fetched successfully")
        return data["text"].strip()
    except Exception as exc:
        logger.exception("Fun fact fetch failed: %s", exc)
        return "Honey never spoils. Archaeologists have found edible honey in ancient tombs."


def get_quote_of_the_day():
    # Real-person quote API (non-AI generated content feed)
    logger.info("Fetching quote of the day")
    try:
        data = _fetch_json("https://zenquotes.io/api/today")
        quote = data[0]
        logger.info("Quote fetched successfully")
        return {"text": quote["q"].strip(), "author": quote["a"].strip()}
    except Exception as exc:
        logger.exception("Quote fetch failed: %s", exc)
        return {
            "text": "Success is the sum of small efforts repeated day in and day out.",
            "author": "Robert Collier",
        }


def generate_daily_content():
    logger.info("Generating AI recommendations for guitar and adventure")
    try:
        ai_data = generate_ai_recommendations()
        logger.info("AI recommendations generated successfully")
    except Exception as exc:
        logger.exception("AI recommendation generation failed: %s", exc)
        ai_data = {
            "song": {
                "title": "Stand by Me",
                "artist": "Ben E. King",
                "difficulty": "easy",
                "chords": "G - Em - C - D",
            },
            "adventure": {
                "name": "Shouf Biosphere Reserve",
                "type": "Hiking",
                "difficulty": "easy",
                "description": "A calm cedar forest route with beautiful mountain air.",
                "country": "Lebanon",
            },
        }

    return {
        "verse": get_verse_of_the_day(),
        "weather": get_weather(),
        "news": get_international_news(),
        "fun_fact": get_fun_fact(),
        "quote": get_quote_of_the_day(),
        "song": ai_data["song"],
        "adventure": ai_data["adventure"],
    }
