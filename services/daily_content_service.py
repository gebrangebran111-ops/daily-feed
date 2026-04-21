import json
import logging
import os
import hashlib
from datetime import date
from urllib import error, request

logger = logging.getLogger("daily_feed")


def _fetch_json(url, headers=None, timeout=20):
    req = request.Request(url, headers=headers or {})
    logger.info("GET %s", url)
    try:
        with request.urlopen(req, timeout=timeout) as response:
            logger.info("Response status: %s", response.status)
            return json.loads(response.read().decode("utf-8"))
    except error.HTTPError as exc:
        logger.error("HTTP error %s for URL: %s", exc.code, url)
        raise
    except error.URLError as exc:
        logger.error("URL error for %s: %s", url, exc.reason)
        raise
    except Exception as exc:
        logger.error("Unexpected error fetching %s: %s", url, exc)
        raise


def _daily_index(seed_extra: str, list_len: int) -> int:
    """Pick a stable index for today that rotates through the list."""
    today_str = date.today().isoformat() + seed_extra
    digest = int(hashlib.md5(today_str.encode()).hexdigest(), 16)
    return digest % list_len


# ---------------------------------------------------------------------------
# Guitar song picks — curated list, rotates daily, no API needed
# ---------------------------------------------------------------------------
_SONGS = [
    {"title": "Wonderwall", "artist": "Oasis", "difficulty": "easy", "chords": "Em7 - G - Dsus4 - A7sus4"},
    {"title": "Let Her Go", "artist": "Passenger", "difficulty": "easy", "chords": "G - D - Em - C"},
    {"title": "Hotel California", "artist": "Eagles", "difficulty": "hard", "chords": "Bm - F# - A - E - G - D - Em - F#"},
    {"title": "Wish You Were Here", "artist": "Pink Floyd", "difficulty": "medium", "chords": "G - Em - A - C"},
    {"title": "Stand by Me", "artist": "Ben E. King", "difficulty": "easy", "chords": "A - F#m - D - E"},
    {"title": "Blackbird", "artist": "The Beatles", "difficulty": "medium", "chords": "G - Am - G/B - C - G"},
    {"title": "More Than Words", "artist": "Extreme", "difficulty": "medium", "chords": "G - G/B - Cadd9 - Am7 - C - D - Em"},
    {"title": "Knockin' on Heaven's Door", "artist": "Bob Dylan", "difficulty": "easy", "chords": "G - D - Am - G - D - C"},
    {"title": "House of the Rising Sun", "artist": "The Animals", "difficulty": "medium", "chords": "Am - C - D - F - Am - E - Am - E"},
    {"title": "Tears in Heaven", "artist": "Eric Clapton", "difficulty": "medium", "chords": "A - E/G# - F#m - A/E - D/F# - E7sus4 - E7"},
    {"title": "Nothing Else Matters", "artist": "Metallica", "difficulty": "medium", "chords": "Em - Am - D - C - G - B7"},
    {"title": "Fast Car", "artist": "Tracy Chapman", "difficulty": "easy", "chords": "Dmaj7 - A - Bm - G"},
    {"title": "Jolene", "artist": "Dolly Parton", "difficulty": "easy", "chords": "Am - C - G - Am"},
    {"title": "Take Me to Church", "artist": "Hozier", "difficulty": "medium", "chords": "Am - F - C - G"},
    {"title": "Somebody That I Used to Know", "artist": "Gotye", "difficulty": "medium", "chords": "Dm - C - Bb - F"},
    {"title": "Mad World", "artist": "Tears for Fears", "difficulty": "easy", "chords": "Dm - G - Bb - F"},
    {"title": "Hallelujah", "artist": "Leonard Cohen", "difficulty": "medium", "chords": "C - Am - C - Am - F - G - C - G"},
    {"title": "The Sound of Silence", "artist": "Simon & Garfunkel", "difficulty": "medium", "chords": "Am - G - Am - C - F - C - Am"},
    {"title": "Redemption Song", "artist": "Bob Marley", "difficulty": "easy", "chords": "G - Em - C - D"},
    {"title": "Brown Eyed Girl", "artist": "Van Morrison", "difficulty": "easy", "chords": "G - C - G - D"},
    {"title": "Africa", "artist": "Toto", "difficulty": "medium", "chords": "F#m - D - A - E"},
    {"title": "Every Rose Has Its Thorn", "artist": "Poison", "difficulty": "easy", "chords": "G - Cadd9 - D - G"},
    {"title": "Behind Blue Eyes", "artist": "The Who", "difficulty": "medium", "chords": "Em - G - D - Dsus4 - C - E"},
    {"title": "Here Comes the Sun", "artist": "The Beatles", "difficulty": "medium", "chords": "D - G - A7 - D"},
    {"title": "Under the Bridge", "artist": "RHCP", "difficulty": "hard", "chords": "D - F# - E - A - G - B - C#m"},
    {"title": "Sweet Home Alabama", "artist": "Lynyrd Skynyrd", "difficulty": "easy", "chords": "D - C - G"},
    {"title": "Creep", "artist": "Radiohead", "difficulty": "easy", "chords": "G - B - C - Cm"},
    {"title": "No Woman No Cry", "artist": "Bob Marley", "difficulty": "easy", "chords": "C - G/B - Am - F - C - G"},
    {"title": "Patience", "artist": "Guns N' Roses", "difficulty": "medium", "chords": "C - G - A - D - C - G - D"},
    {"title": "Stairway to Heaven", "artist": "Led Zeppelin", "difficulty": "hard", "chords": "Am - Am/G# - Am/G - D/F# - Fmaj7 - G - Am"},
    {"title": "Angie", "artist": "Rolling Stones", "difficulty": "medium", "chords": "Am - E7 - Gsus4 - G - F - C - Dm"},
    {"title": "Wonderwall", "artist": "Oasis", "difficulty": "easy", "chords": "Em7 - G - Dsus4 - A7sus4"},
    {"title": "Shape of You", "artist": "Ed Sheeran", "difficulty": "easy", "chords": "C#m - F#m - A - B"},
    {"title": "Perfect", "artist": "Ed Sheeran", "difficulty": "easy", "chords": "G - Em - C - D"},
    {"title": "Riptide", "artist": "Vance Joy", "difficulty": "easy", "chords": "Am - G - C"},
    {"title": "Hey There Delilah", "artist": "Plain White T's", "difficulty": "easy", "chords": "D - F#m - Bm - G - A"},
    {"title": "Country Roads", "artist": "John Denver", "difficulty": "easy", "chords": "G - D - Em - C"},
    {"title": "Hotel California", "artist": "Eagles", "difficulty": "hard", "chords": "Bm - F# - A - E - G - D - Em - F#"},
    {"title": "Lose Yourself", "artist": "Eminem", "difficulty": "medium", "chords": "Dm - Bb - C - Dm"},
    {"title": "Yesterday", "artist": "The Beatles", "difficulty": "medium", "chords": "F - Em - A7 - Dm - Bb - C7 - F"},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "difficulty": "easy", "chords": "F - Bb - Ab - Db"},
    {"title": "With or Without You", "artist": "U2", "difficulty": "easy", "chords": "D - A - Bm - G"},
    {"title": "Man in the Mirror", "artist": "Michael Jackson", "difficulty": "medium", "chords": "G - Am - C - D"},
    {"title": "Shallow", "artist": "Lady Gaga & Bradley Cooper", "difficulty": "medium", "chords": "Em - D - G - C"},
    {"title": "River", "artist": "Leon Bridges", "difficulty": "medium", "chords": "A - Asus2 - D - F#m - E"},
    {"title": "Gravity", "artist": "John Mayer", "difficulty": "medium", "chords": "G - Gsus4 - C - D/F# - Em - A7"},
    {"title": "Blackbird", "artist": "The Beatles", "difficulty": "medium", "chords": "G - Am7 - G/B - C - G"},
    {"title": "The A Team", "artist": "Ed Sheeran", "difficulty": "easy", "chords": "A - E/G# - F#m - D - A/C# - E"},
    {"title": "Banana Pancakes", "artist": "Jack Johnson", "difficulty": "easy", "chords": "G - C - D - Am"},
    {"title": "Demons", "artist": "Imagine Dragons", "difficulty": "easy", "chords": "C - D - G - Em"},
]

# ---------------------------------------------------------------------------
# Lebanon adventure picks — curated list, rotates daily, no API needed
# ---------------------------------------------------------------------------
_ADVENTURES = [
    {"name": "Qadisha Valley", "type": "Hiking", "difficulty": "medium", "description": "A UNESCO World Heritage gorge with ancient monasteries carved into the cliffs and cedar forests above."},
    {"name": "Shouf Cedar Reserve", "type": "Hiking", "difficulty": "easy", "description": "Lebanon's largest nature reserve, home to ancient cedars and stunning mountain panoramas."},
    {"name": "Tannourine Cedar Forest", "type": "Hiking", "difficulty": "easy", "description": "A pristine cedar nature reserve with marked trails and dramatic rock formations."},
    {"name": "Jabal Sannine", "type": "Hiking", "difficulty": "hard", "description": "One of Lebanon's highest peaks with sweeping views of the Bekaa Valley and the Mediterranean."},
    {"name": "Wadi Nahr Ibrahim", "type": "Hiking", "difficulty": "medium", "description": "A lush river valley with waterfalls, ancient ruins, and natural swimming pools."},
    {"name": "Falougha Pine Forests", "type": "Hiking/Camping", "difficulty": "easy", "description": "Cool pine-scented trails and open camping grounds, perfect for escaping Beirut's summer heat."},
    {"name": "Horsh Ehden Nature Reserve", "type": "Hiking", "difficulty": "easy", "description": "A biodiversity hotspot in the north with wildflowers, ancient oaks, and rare bird species."},
    {"name": "Laklouk Plateau", "type": "Hiking", "difficulty": "medium", "description": "A high-altitude plateau with rare flora, caves, and panoramic views over the Byblos coast."},
    {"name": "Wadi Qannoubin", "type": "Hiking", "difficulty": "medium", "description": "A sacred valley in the Qadisha with cave hermitages and Byzantine inscriptions in the rock."},
    {"name": "Barouk Cedar Forest", "type": "Hiking", "difficulty": "easy", "description": "Part of the Shouf Biosphere Reserve with gentle trails among some of Lebanon's oldest cedars."},
    {"name": "Niha Fortress", "type": "Hiking", "difficulty": "medium", "description": "A Crusader-era castle perched on a cliff in the Bekaa with sweeping valley views."},
    {"name": "Baskinta Literary Trail", "type": "Hiking", "difficulty": "easy", "description": "A scenic village trail linking stone houses, olive groves, and heritage sites in Mount Lebanon."},
    {"name": "Akkar Forest", "type": "Hiking/Camping", "difficulty": "medium", "description": "Remote northern wilderness with dense oak forests, rivers, and almost no tourist crowds."},
    {"name": "Aammiq Wetland", "type": "Hiking", "difficulty": "easy", "description": "Lebanon's last major freshwater wetland, a paradise for birdwatching and nature photography."},
    {"name": "Jabal Moussa", "type": "Hiking", "difficulty": "medium", "description": "A UNESCO Biosphere Reserve near Byblos with dramatic ridgelines and Mediterranean scrubland."},
    {"name": "Wadi el Deir", "type": "Hiking", "difficulty": "medium", "description": "A hidden valley in Baskinta with a rushing stream, terraced orchards, and old stone bridges."},
    {"name": "Bcharre to Qadisha Gorge Trail", "type": "Hiking", "difficulty": "hard", "description": "A challenging descent into the Qadisha Gorge from the Christian heartland of Bcharre."},
    {"name": "Ehden to Arz Trail", "type": "Hiking", "difficulty": "medium", "description": "A classic north Lebanon trail linking the beautiful village of Ehden to the cedar forests."},
    {"name": "Kfardebian to Jabal Sannine", "type": "Hiking", "difficulty": "hard", "description": "A high mountain traverse over rocky limestone ridges with breathtaking 360-degree views."},
    {"name": "Maasser el Chouf", "type": "Hiking", "difficulty": "easy", "description": "Gateway village to the Shouf Reserve with cedar groves, wildflowers, and welcoming guesthouses."},
    {"name": "Beaufort Castle Trail", "type": "Hiking", "difficulty": "easy", "description": "A walk to a dramatic Crusader castle in south Lebanon overlooking the Litani River valley."},
    {"name": "Harajel Pine Forest", "type": "Camping", "difficulty": "easy", "description": "A cool mountain forest east of Beirut with designated camping spots and fragrant pine air."},
    {"name": "Yahchouch to Faqra", "type": "Hiking", "difficulty": "medium", "description": "A high-altitude trail connecting two mountain villages past Roman temples and snow patches."},
    {"name": "Deir el Qamar to Beiteddine", "type": "Hiking", "difficulty": "easy", "description": "A scenic historic trail through the heart of the Chouf, passing Ottoman-era architecture."},
    {"name": "Wadi Mseilha", "type": "Hiking", "difficulty": "easy", "description": "A dramatic limestone canyon in north Lebanon with a striking Mamluk-era fortress on a lone rock."},
    {"name": "Douma Village Trails", "type": "Hiking", "difficulty": "easy", "description": "A beautifully preserved mountain village with Ottoman stone houses and vineyard walking routes."},
    {"name": "Jezzine Forest Walks", "type": "Hiking", "difficulty": "easy", "description": "Pine and cedar forests above the famous Bisri waterfall, ideal for peaceful morning hikes."},
    {"name": "Tyre Coast Nature Reserve", "type": "Hiking", "difficulty": "easy", "description": "Lebanon's only sandy beach nature reserve, nesting ground for loggerhead sea turtles."},
    {"name": "Laqlouq to Jabal Kneisseh", "type": "Hiking", "difficulty": "hard", "description": "A rugged high-mountain trail across the spine of Mount Lebanon with extreme panoramic views."},
    {"name": "Cedars of God, Bcharre", "type": "Hiking", "difficulty": "easy", "description": "Walk among the most ancient cedar trees in Lebanon, some over 3,000 years old, near Bcharre."},
]


def get_song_of_the_day():
    logger.info("--- Picking: Guitar Song of the Day ---")
    idx = _daily_index("song", len(_SONGS))
    song = _SONGS[idx]
    logger.info("Song pick: %s by %s", song["title"], song["artist"])
    return song


def get_adventure_of_the_day():
    logger.info("--- Picking: Adventure of the Day ---")
    idx = _daily_index("adventure", len(_ADVENTURES))
    adventure = _ADVENTURES[idx]
    logger.info("Adventure pick: %s", adventure["name"])
    return adventure


# ---------------------------------------------------------------------------
# External API fetches
# ---------------------------------------------------------------------------

_BOOK_NAMES = {
    1: "Genesis", 2: "Exodus", 3: "Leviticus", 4: "Numbers", 5: "Deuteronomy",
    6: "Joshua", 7: "Judges", 8: "Ruth", 9: "1 Samuel", 10: "2 Samuel",
    11: "1 Kings", 12: "2 Kings", 13: "1 Chronicles", 14: "2 Chronicles",
    15: "Ezra", 16: "Nehemiah", 17: "Esther", 18: "Job", 19: "Psalms",
    20: "Proverbs", 21: "Ecclesiastes", 22: "Song of Solomon", 23: "Isaiah",
    24: "Jeremiah", 25: "Lamentations", 26: "Ezekiel", 27: "Daniel",
    28: "Hosea", 29: "Joel", 30: "Amos", 31: "Obadiah", 32: "Jonah",
    33: "Micah", 34: "Nahum", 35: "Habakkuk", 36: "Zephaniah", 37: "Haggai",
    38: "Zechariah", 39: "Malachi", 40: "Matthew", 41: "Mark", 42: "Luke",
    43: "John", 44: "Acts", 45: "Romans", 46: "1 Corinthians",
    47: "2 Corinthians", 48: "Galatians", 49: "Ephesians", 50: "Philippians",
    51: "Colossians", 52: "1 Thessalonians", 53: "2 Thessalonians",
    54: "1 Timothy", 55: "2 Timothy", 56: "Titus", 57: "Philemon",
    58: "Hebrews", 59: "James", 60: "1 Peter", 61: "2 Peter",
    62: "1 John", 63: "2 John", 64: "3 John", 65: "Jude", 66: "Revelation",
}


def get_verse_of_the_day():
    logger.info("--- Fetching: Verse of the Day ---")
    try:
        data = _fetch_json("https://bolls.life/get-random-verse/NIV/")
        book_name = _BOOK_NAMES.get(data["book"], f"Book {data['book']}")
        reference = f"{book_name} {data['chapter']}:{data['verse']}"
        text = (
            data["text"]
            .replace("<p>", "").replace("</p>", "")
            .replace("<i>", "").replace("</i>", "")
            .strip()
        )
        logger.info("Verse fetched: %s", reference)
        return {"text": text, "reference": reference}
    except Exception as exc:
        logger.error("Verse fetch failed: %s", exc)
        logger.warning("FALLBACK triggered for verse")
        return {"text": "Verse unavailable today.", "reference": "—"}


def _weather_label(code):
    return {
        0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Foggy", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
        55: "Dense drizzle", 61: "Slight rain", 63: "Rain", 65: "Heavy rain",
        80: "Rain showers", 81: "Rain showers", 82: "Heavy rain showers",
        95: "Thunderstorm",
    }.get(code, "Mixed weather")


def _weather_emoji(code):
    if code == 0: return "☀️"
    if code == 1: return "🌤️"
    if code == 2: return "⛅"
    if code == 3: return "☁️"
    if code in (45, 48): return "🌫️"
    if code in (51, 53, 55, 61, 63, 65, 80, 81, 82): return "🌧️"
    if code == 95: return "⛈️"
    return "🌡️"


def get_weather():
    logger.info("--- Fetching: Weather ---")
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
            code = daily["weathercode"][i]
            days.append({
                "date": daily["time"][i],
                "condition": _weather_label(code),
                "emoji": _weather_emoji(code),
                "temp_max": round(daily["temperature_2m_max"][i]),
                "temp_min": round(daily["temperature_2m_min"][i]),
                "rain_mm": round(daily["precipitation_sum"][i], 1),
            })
        logger.info("Weather fetched successfully")
        return {"city": "Beirut, Lebanon", "days": days}
    except Exception as exc:
        logger.error("Weather fetch failed: %s", exc)
        logger.warning("FALLBACK triggered for weather")
        return {
            "city": "Beirut, Lebanon",
            "days": [
                {"date": "Today", "condition": "Unavailable", "emoji": "🌡️", "temp_max": "—", "temp_min": "—", "rain_mm": "—"},
                {"date": "Tomorrow", "condition": "Unavailable", "emoji": "🌡️", "temp_max": "—", "temp_min": "—", "rain_mm": "—"},
            ],
        }


def get_international_news():
    logger.info("--- Fetching: International News ---")
    api_key = os.getenv("GNEWS_API_KEY")
    if not api_key:
        logger.error("GNEWS_API_KEY env variable is missing")
        return {"headlines": [{"title": "News unavailable (GNEWS_API_KEY not configured).", "source": "—", "url": ""}]}

    url = f"https://gnews.io/api/v4/top-headlines?category=general&lang=en&max=3&apikey={api_key}"
    try:
        data = _fetch_json(url)
        articles = data.get("articles", [])
        if not articles:
            raise ValueError("No articles returned from GNews API")
        headlines = [
            {
                "title": a["title"].strip(),
                "source": a.get("source", {}).get("name", "Unknown").strip(),
                "url": a.get("url", "").strip(),
            }
            for a in articles[:3]
        ]
        logger.info("News fetched: %d headlines", len(headlines))
        return {"headlines": headlines}
    except Exception as exc:
        logger.error("News fetch failed: %s", exc)
        logger.warning("FALLBACK triggered for news")
        return {"headlines": [{"title": "News unavailable.", "source": "—", "url": ""}]}


def get_fun_fact():
    logger.info("--- Fetching: Fun Fact ---")
    try:
        data = _fetch_json("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
        logger.info("Fun fact fetched successfully")
        return data["text"].strip()
    except Exception as exc:
        logger.error("Fun fact fetch failed: %s", exc)
        logger.warning("FALLBACK triggered for fun fact")
        return "Fun fact unavailable today."


def get_quote_of_the_day():
    # api.quotable.io — free, no key, 180 req/min limit, truly random
    logger.info("--- Fetching: Quote of the Day ---")
    try:
        data = _fetch_json("https://api.quotable.io/quotes/random?tags=inspirational|wisdom|success")
        quote = data[0]
        logger.info("Quote fetched: %s", quote.get("author"))
        return {"text": quote["content"].strip(), "author": quote["author"].strip()}
    except Exception as exc:
        logger.error("Quote fetch failed: %s", exc)
        logger.warning("FALLBACK triggered for quote")
        return {"text": "Quote unavailable today.", "author": "—"}


def generate_daily_content():
    return {
        "verse": get_verse_of_the_day(),
        "weather": get_weather(),
        "news": get_international_news(),
        "fun_fact": get_fun_fact(),
        "quote": get_quote_of_the_day(),
        "song": get_song_of_the_day(),
        "adventure": get_adventure_of_the_day(),
    }
