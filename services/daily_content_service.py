import json
import os
from urllib import parse, request


def _fetch_json(url, headers=None, timeout=20):
    req = request.Request(url, headers=headers or {})
    with request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def get_verse_of_the_day():
    try:
        data = _fetch_json("https://beta.ourmanna.com/api/v1/get/?format=json")
        details = data["verse"]["details"]
        return {
            "text": details["text"].strip(),
            "reference": details["reference"].strip(),
        }
    except Exception:
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
        return {"city": "Beirut, Lebanon", "days": days}
    except Exception:
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
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        return {
            "title": "International news is unavailable (missing NEWSAPI_KEY).",
            "source": "Setup needed",
            "url": "",
        }

    query = parse.urlencode(
        {
            "q": "international OR global OR world",
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 1,
        }
    )
    url = f"https://newsapi.org/v2/everything?{query}"
    try:
        data = _fetch_json(url, headers={"X-Api-Key": api_key})
        article = data["articles"][0]
        return {
            "title": article["title"],
            "source": article["source"]["name"],
            "url": article.get("url", ""),
        }
    except Exception:
        return {
            "title": "Could not fetch international news right now.",
            "source": "News API",
            "url": "",
        }


def get_fun_fact():
    try:
        data = _fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        return data["text"].strip()
    except Exception:
        return "Honey never spoils. Archaeologists have found edible honey in ancient tombs."


def get_quote_of_the_day():
    # Real-person quote API (non-AI generated content feed)
    try:
        data = _fetch_json("https://zenquotes.io/api/today")
        quote = data[0]
        return {"text": quote["q"].strip(), "author": quote["a"].strip()}
    except Exception:
        return {
            "text": "Success is the sum of small efforts repeated day in and day out.",
            "author": "Robert Collier",
        }


def generate_daily_content():
    return {
        "verse": get_verse_of_the_day(),
        "weather": get_weather(),
        "news": get_international_news(),
        "fun_fact": get_fun_fact(),
        "quote": get_quote_of_the_day(),
    }
