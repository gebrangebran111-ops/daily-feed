import hashlib
import json
import logging
import os
from datetime import date
from urllib import error, request

logger = logging.getLogger(“daily_feed”)

def _fetch_json(url, headers=None, timeout=20):
req = request.Request(url, headers=headers or {})
logger.info(“GET %s”, url)
try:
with request.urlopen(req, timeout=timeout) as response:
logger.info(“Response status: %s”, response.status)
return json.loads(response.read().decode(“utf-8”))
except error.HTTPError as exc:
logger.error(“HTTP error %s for URL: %s”, exc.code, url)
raise
except error.URLError as exc:
logger.error(“URL error for %s: %s”, url, exc.reason)
raise
except Exception as exc:
logger.error(“Unexpected error fetching %s: %s”, url, exc)
raise

def _daily_index(seed_extra: str, list_len: int) -> int:
“”“Returns a stable index for today that rotates through the list each day.”””
today_str = date.today().isoformat() + seed_extra
return int(hashlib.md5(today_str.encode()).hexdigest(), 16) % list_len

# ── Quotes — curated, rotates daily, no API needed ──────────────────────────

_QUOTES = [
{“text”: “The only way to do great work is to love what you do.”, “author”: “Steve Jobs”},
{“text”: “In the middle of every difficulty lies opportunity.”, “author”: “Albert Einstein”},
{“text”: “It does not matter how slowly you go as long as you do not stop.”, “author”: “Confucius”},
{“text”: “Life is what happens when you’re busy making other plans.”, “author”: “John Lennon”},
{“text”: “The future belongs to those who believe in the beauty of their dreams.”, “author”: “Eleanor Roosevelt”},
{“text”: “Success is not final, failure is not fatal: it is the courage to continue that counts.”, “author”: “Winston Churchill”},
{“text”: “You miss 100% of the shots you don’t take.”, “author”: “Wayne Gretzky”},
{“text”: “Whether you think you can or you think you can’t, you’re right.”, “author”: “Henry Ford”},
{“text”: “The only impossible journey is the one you never begin.”, “author”: “Tony Robbins”},
{“text”: “Do what you can, with what you have, where you are.”, “author”: “Theodore Roosevelt”},
{“text”: “Darkness cannot drive out darkness; only light can do that.”, “author”: “Martin Luther King Jr.”},
{“text”: “The greatest glory in living lies not in never falling, but in rising every time we fall.”, “author”: “Nelson Mandela”},
{“text”: “Spread love everywhere you go. Let no one ever come to you without leaving happier.”, “author”: “Mother Teresa”},
{“text”: “When you reach the end of your rope, tie a knot in it and hang on.”, “author”: “Franklin D. Roosevelt”},
{“text”: “Always remember that you are absolutely unique. Just like everyone else.”, “author”: “Margaret Mead”},
{“text”: “Don’t judge each day by the harvest you reap but by the seeds that you plant.”, “author”: “Robert Louis Stevenson”},
{“text”: “The purpose of our lives is to be happy.”, “author”: “Dalai Lama”},
{“text”: “Get busy living or get busy dying.”, “author”: “Stephen King”},
{“text”: “You only live once, but if you do it right, once is enough.”, “author”: “Mae West”},
{“text”: “Many of life’s failures are people who did not realize how close they were to success when they gave up.”, “author”: “Thomas A. Edison”},
{“text”: “You have brains in your head. You have feet in your shoes. You can steer yourself any direction you choose.”, “author”: “Dr. Seuss”},
{“text”: “If life were predictable it would cease to be life, and be without flavor.”, “author”: “Eleanor Roosevelt”},
{“text”: “If you look at what you have in life, you’ll always have more.”, “author”: “Oprah Winfrey”},
{“text”: “If you want to live a happy life, tie it to a goal, not to people or things.”, “author”: “Albert Einstein”},
{“text”: “Never let the fear of striking out keep you from playing the game.”, “author”: “Babe Ruth”},
{“text”: “Money and success don’t change people; they merely amplify what is already there.”, “author”: “Will Smith”},
{“text”: “Your time is limited, so don’t waste it living someone else’s life.”, “author”: “Steve Jobs”},
{“text”: “Not how long, but how well you have lived is the main thing.”, “author”: “Seneca”},
{“text”: “If life is not a great adventure, it is nothing.”, “author”: “Helen Keller”},
{“text”: “Challenges are what make life interesting and overcoming them is what makes life meaningful.”, “author”: “Joshua J. Marine”},
{“text”: “If you want to achieve greatness stop asking for permission.”, “author”: “Anonymous”},
{“text”: “Things work out best for those who make the best of how things work out.”, “author”: “John Wooden”},
{“text”: “To live a creative life, we must lose our fear of being wrong.”, “author”: “Anonymous”},
{“text”: “If you are not willing to risk the usual, you will have to settle for the ordinary.”, “author”: “Jim Rohn”},
{“text”: “Trust because you are willing to accept the risk, not because it’s safe or certain.”, “author”: “Anonymous”},
{“text”: “Take up one idea. Make that one idea your life — think of it, dream of it, live on that idea.”, “author”: “Swami Vivekananda”},
{“text”: “All our dreams can come true, if we have the courage to pursue them.”, “author”: “Walt Disney”},
{“text”: “Good things come to people who wait, but better things come to those who go out and get them.”, “author”: “Anonymous”},
{“text”: “If you do what you always did, you will get what you always got.”, “author”: “Anonymous”},
{“text”: “Success is walking from failure to failure with no loss of enthusiasm.”, “author”: “Winston Churchill”},
{“text”: “Just when the caterpillar thought the world was ending, he turned into a butterfly.”, “author”: “Anonymous”},
{“text”: “Successful entrepreneurs are givers and not takers of positive energy.”, “author”: “Anonymous”},
{“text”: “Whenever you see a successful person, you only see the public glories, never the private sacrifices.”, “author”: “Vaibhav Shah”},
{“text”: “Opportunities don’t happen, you create them.”, “author”: “Chris Grosser”},
{“text”: “Try not to become a person of success, but rather try to become a person of value.”, “author”: “Albert Einstein”},
{“text”: “Great minds discuss ideas; average minds discuss events; small minds discuss people.”, “author”: “Eleanor Roosevelt”},
{“text”: “I have not failed. I’ve just found 10,000 ways that won’t work.”, “author”: “Thomas A. Edison”},
{“text”: “If you don’t value your time, neither will others. Stop giving away your time and talents.”, “author”: “Kim Garst”},
{“text”: “A successful man is one who can lay a firm foundation with the bricks others have thrown at him.”, “author”: “David Brinkley”},
{“text”: “No one can make you feel inferior without your consent.”, “author”: “Eleanor Roosevelt”},
{“text”: “The whole secret of a successful life is to find out what is one’s destiny to do, and then do it.”, “author”: “Henry Ford”},
{“text”: “If you’re going through hell, keep going.”, “author”: “Winston Churchill”},
{“text”: “The ones who are crazy enough to think they can change the world, are the ones who do.”, “author”: “Anonymous”},
{“text”: “Don’t raise your voice, improve your argument.”, “author”: “Desmond Tutu”},
{“text”: “What seems to us as bitter trials are often blessings in disguise.”, “author”: “Oscar Wilde”},
{“text”: “The meaning of life is to find your gift. The purpose of life is to give it away.”, “author”: “Anonymous”},
{“text”: “The distance between insanity and genius is measured only by success.”, “author”: “Bruce Feirstein”},
{“text”: “Don’t be afraid to give up the good to go for the great.”, “author”: “John D. Rockefeller”},
{“text”: “There are two types of people who will tell you that you cannot make a difference in this world: those who are afraid to try and those who are afraid you will succeed.”, “author”: “Ray Goforth”},
{“text”: “Believe you can and you’re halfway there.”, “author”: “Theodore Roosevelt”},
{“text”: “The secret of getting ahead is getting started.”, “author”: “Mark Twain”},
{“text”: “I can’t change the direction of the wind, but I can adjust my sails to always reach my destination.”, “author”: “Jimmy Dean”},
{“text”: “You can’t use up creativity. The more you use, the more you have.”, “author”: “Maya Angelou”},
{“text”: “Either write something worth reading or do something worth writing.”, “author”: “Benjamin Franklin”},
{“text”: “Innovation distinguishes between a leader and a follower.”, “author”: “Steve Jobs”},
{“text”: “There is only one way to avoid criticism: do nothing, say nothing, and be nothing.”, “author”: “Aristotle”},
{“text”: “Ask and it will be given to you; search, and you will find; knock and the door will be opened for you.”, “author”: “Jesus”},
{“text”: “The more that you read, the more things you will know.”, “author”: “Dr. Seuss”},
{“text”: “I am not a product of my circumstances. I am a product of my decisions.”, “author”: “Stephen Covey”},
{“text”: “When I stand before God at the end of my life, I hope that I would not have a single bit of talent left.”, “author”: “Erma Bombeck”},
{“text”: “Definitions belong to the definers, not the defined.”, “author”: “Toni Morrison”},
{“text”: “Work like there is someone working 24 hours a day to take everything away from you.”, “author”: “Mark Cuban”},
{“text”: “What you lack in talent can be made up with desire, hustle and giving 110% all the time.”, “author”: “Don Zimmer”},
{“text”: “Things may come to those who wait, but only the things left by those who hustle.”, “author”: “Abraham Lincoln”},
{“text”: “Without hustle, talent will only carry you so far.”, “author”: “Gary Vaynerchuk”},
{“text”: “There are no traffic jams along the extra mile.”, “author”: “Roger Staubach”},
{“text”: “Motivation is what gets you started. Habit is what keeps you going.”, “author”: “Jim Ryun”},
]

# ── Guitar song picks — curated, rotates daily ───────────────────────────────

_SONGS = [
{“title”: “Wonderwall”, “artist”: “Oasis”, “difficulty”: “easy”, “chords”: “Em7 - G - Dsus4 - A7sus4”},
{“title”: “Let Her Go”, “artist”: “Passenger”, “difficulty”: “easy”, “chords”: “G - D - Em - C”},
{“title”: “Hotel California”, “artist”: “Eagles”, “difficulty”: “hard”, “chords”: “Bm - F# - A - E - G - D - Em - F#”},
{“title”: “Wish You Were Here”, “artist”: “Pink Floyd”, “difficulty”: “medium”, “chords”: “G - Em - A - C”},
{“title”: “Stand by Me”, “artist”: “Ben E. King”, “difficulty”: “easy”, “chords”: “A - F#m - D - E”},
{“title”: “Blackbird”, “artist”: “The Beatles”, “difficulty”: “medium”, “chords”: “G - Am - G/B - C - G”},
{“title”: “More Than Words”, “artist”: “Extreme”, “difficulty”: “medium”, “chords”: “G - G/B - Cadd9 - Am7 - C - D - Em”},
{“title”: “Knockin’ on Heaven’s Door”, “artist”: “Bob Dylan”, “difficulty”: “easy”, “chords”: “G - D - Am - G - D - C”},
{“title”: “House of the Rising Sun”, “artist”: “The Animals”, “difficulty”: “medium”, “chords”: “Am - C - D - F - Am - E”},
{“title”: “Tears in Heaven”, “artist”: “Eric Clapton”, “difficulty”: “medium”, “chords”: “A - E/G# - F#m - A/E - D/F# - E7”},
{“title”: “Nothing Else Matters”, “artist”: “Metallica”, “difficulty”: “medium”, “chords”: “Em - Am - D - C - G - B7”},
{“title”: “Fast Car”, “artist”: “Tracy Chapman”, “difficulty”: “easy”, “chords”: “Dmaj7 - A - Bm - G”},
{“title”: “Jolene”, “artist”: “Dolly Parton”, “difficulty”: “easy”, “chords”: “Am - C - G - Am”},
{“title”: “Take Me to Church”, “artist”: “Hozier”, “difficulty”: “medium”, “chords”: “Am - F - C - G”},
{“title”: “Mad World”, “artist”: “Tears for Fears”, “difficulty”: “easy”, “chords”: “Dm - G - Bb - F”},
{“title”: “Hallelujah”, “artist”: “Leonard Cohen”, “difficulty”: “medium”, “chords”: “C - Am - F - G”},
{“title”: “The Sound of Silence”, “artist”: “Simon & Garfunkel”, “difficulty”: “medium”, “chords”: “Am - G - C - F”},
{“title”: “Redemption Song”, “artist”: “Bob Marley”, “difficulty”: “easy”, “chords”: “G - Em - C - D”},
{“title”: “Brown Eyed Girl”, “artist”: “Van Morrison”, “difficulty”: “easy”, “chords”: “G - C - G - D”},
{“title”: “Africa”, “artist”: “Toto”, “difficulty”: “medium”, “chords”: “F#m - D - A - E”},
{“title”: “Behind Blue Eyes”, “artist”: “The Who”, “difficulty”: “medium”, “chords”: “Em - G - D - C - E”},
{“title”: “Here Comes the Sun”, “artist”: “The Beatles”, “difficulty”: “medium”, “chords”: “D - G - A7”},
{“title”: “Under the Bridge”, “artist”: “RHCP”, “difficulty”: “hard”, “chords”: “D - F# - E - A - G - B - C#m”},
{“title”: “Sweet Home Alabama”, “artist”: “Lynyrd Skynyrd”, “difficulty”: “easy”, “chords”: “D - C - G”},
{“title”: “Creep”, “artist”: “Radiohead”, “difficulty”: “easy”, “chords”: “G - B - C - Cm”},
{“title”: “No Woman No Cry”, “artist”: “Bob Marley”, “difficulty”: “easy”, “chords”: “C - G/B - Am - F - C - G”},
{“title”: “Patience”, “artist”: “Guns N’ Roses”, “difficulty”: “medium”, “chords”: “C - G - A - D”},
{“title”: “Shape of You”, “artist”: “Ed Sheeran”, “difficulty”: “easy”, “chords”: “C#m - F#m - A - B”},
{“title”: “Perfect”, “artist”: “Ed Sheeran”, “difficulty”: “easy”, “chords”: “G - Em - C - D”},
{“title”: “Riptide”, “artist”: “Vance Joy”, “difficulty”: “easy”, “chords”: “Am - G - C”},
{“title”: “Hey There Delilah”, “artist”: “Plain White T’s”, “difficulty”: “easy”, “chords”: “D - F#m - Bm - G - A”},
{“title”: “Country Roads”, “artist”: “John Denver”, “difficulty”: “easy”, “chords”: “G - D - Em - C”},
{“title”: “Yesterday”, “artist”: “The Beatles”, “difficulty”: “medium”, “chords”: “F - Em - A7 - Dm - Bb - C7”},
{“title”: “Smells Like Teen Spirit”, “artist”: “Nirvana”, “difficulty”: “easy”, “chords”: “F - Bb - Ab - Db”},
{“title”: “With or Without You”, “artist”: “U2”, “difficulty”: “easy”, “chords”: “D - A - Bm - G”},
{“title”: “Shallow”, “artist”: “Lady Gaga & Bradley Cooper”, “difficulty”: “medium”, “chords”: “Em - D - G - C”},
{“title”: “Gravity”, “artist”: “John Mayer”, “difficulty”: “medium”, “chords”: “G - Gsus4 - C - D/F# - Em - A7”},
{“title”: “The A Team”, “artist”: “Ed Sheeran”, “difficulty”: “easy”, “chords”: “A - E/G# - F#m - D”},
{“title”: “Banana Pancakes”, “artist”: “Jack Johnson”, “difficulty”: “easy”, “chords”: “G - C - D - Am”},
{“title”: “Demons”, “artist”: “Imagine Dragons”, “difficulty”: “easy”, “chords”: “C - D - G - Em”},
{“title”: “River”, “artist”: “Leon Bridges”, “difficulty”: “medium”, “chords”: “A - Asus2 - D - F#m - E”},
{“title”: “Stairway to Heaven”, “artist”: “Led Zeppelin”, “difficulty”: “hard”, “chords”: “Am - Am/G# - Am/G - D/F# - Fmaj7 - G”},
{“title”: “Angie”, “artist”: “Rolling Stones”, “difficulty”: “medium”, “chords”: “Am - E7 - G - F - C - Dm”},
{“title”: “Lose Yourself”, “artist”: “Eminem”, “difficulty”: “medium”, “chords”: “Dm - Bb - C”},
{“title”: “Somebody That I Used to Know”, “artist”: “Gotye”, “difficulty”: “medium”, “chords”: “Dm - C - Bb - F”},
{“title”: “Every Rose Has Its Thorn”, “artist”: “Poison”, “difficulty”: “easy”, “chords”: “G - Cadd9 - D”},
{“title”: “Man in the Mirror”, “artist”: “Michael Jackson”, “difficulty”: “medium”, “chords”: “G - Am - C - D”},
{“title”: “Fast Car”, “artist”: “Tracy Chapman”, “difficulty”: “easy”, “chords”: “Dmaj7 - A - Bm - G”},
{“title”: “No Rain”, “artist”: “Blind Melon”, “difficulty”: “easy”, “chords”: “E - A - D - A”},
{“title”: “Wonderwall”, “artist”: “Oasis”, “difficulty”: “easy”, “chords”: “Em7 - G - Dsus4 - A7sus4”},
]

# ── Lebanon adventures — curated, rotates daily ──────────────────────────────

_ADVENTURES = [
{“name”: “Qadisha Valley”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A UNESCO World Heritage gorge with ancient monasteries carved into the cliffs and cedar forests above.”},
{“name”: “Shouf Cedar Reserve”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Lebanon’s largest nature reserve, home to ancient cedars and stunning mountain panoramas.”},
{“name”: “Tannourine Cedar Forest”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A pristine cedar nature reserve with marked trails and dramatic rock formations.”},
{“name”: “Jabal Sannine”, “type”: “Hiking”, “difficulty”: “hard”, “description”: “One of Lebanon’s highest peaks with sweeping views of the Bekaa Valley and the Mediterranean.”},
{“name”: “Wadi Nahr Ibrahim”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A lush river valley with waterfalls, ancient ruins, and natural swimming pools.”},
{“name”: “Falougha Pine Forests”, “type”: “Hiking/Camping”, “difficulty”: “easy”, “description”: “Cool pine-scented trails and open camping grounds, perfect for escaping Beirut’s heat.”},
{“name”: “Horsh Ehden Nature Reserve”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A biodiversity hotspot in the north with wildflowers, ancient oaks, and rare bird species.”},
{“name”: “Laklouk Plateau”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A high-altitude plateau with rare flora, caves, and panoramic views over the Byblos coast.”},
{“name”: “Wadi Qannoubin”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A sacred valley in the Qadisha with cave hermitages and Byzantine inscriptions in the rock.”},
{“name”: “Barouk Cedar Forest”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Part of the Shouf Biosphere Reserve with gentle trails among some of Lebanon’s oldest cedars.”},
{“name”: “Niha Fortress”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A Crusader-era castle perched on a cliff in the Bekaa with sweeping valley views.”},
{“name”: “Baskinta Literary Trail”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A scenic village trail linking stone houses, olive groves, and heritage sites in Mount Lebanon.”},
{“name”: “Akkar Forest”, “type”: “Hiking/Camping”, “difficulty”: “medium”, “description”: “Remote northern wilderness with dense oak forests, rivers, and almost no tourist crowds.”},
{“name”: “Aammiq Wetland”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Lebanon’s last major freshwater wetland, a paradise for birdwatching and nature photography.”},
{“name”: “Jabal Moussa”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A UNESCO Biosphere Reserve near Byblos with dramatic ridgelines and Mediterranean scrubland.”},
{“name”: “Wadi el Deir”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A hidden valley in Baskinta with a rushing stream, terraced orchards, and old stone bridges.”},
{“name”: “Bcharre to Qadisha Gorge Trail”, “type”: “Hiking”, “difficulty”: “hard”, “description”: “A challenging descent into the Qadisha Gorge from the Christian heartland of Bcharre.”},
{“name”: “Ehden to Arz Trail”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A classic north Lebanon trail linking the beautiful village of Ehden to the cedar forests.”},
{“name”: “Kfardebian to Jabal Sannine”, “type”: “Hiking”, “difficulty”: “hard”, “description”: “A high mountain traverse over rocky limestone ridges with breathtaking 360-degree views.”},
{“name”: “Maasser el Chouf”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Gateway village to the Shouf Reserve with cedar groves, wildflowers, and welcoming guesthouses.”},
{“name”: “Beaufort Castle Trail”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A walk to a dramatic Crusader castle in south Lebanon overlooking the Litani River valley.”},
{“name”: “Harajel Pine Forest”, “type”: “Camping”, “difficulty”: “easy”, “description”: “A cool mountain forest east of Beirut with designated camping spots and fragrant pine air.”},
{“name”: “Yahchouch to Faqra”, “type”: “Hiking”, “difficulty”: “medium”, “description”: “A high-altitude trail connecting two mountain villages past Roman temples and snow patches.”},
{“name”: “Deir el Qamar to Beiteddine”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A scenic historic trail through the heart of the Chouf, passing Ottoman-era architecture.”},
{“name”: “Wadi Mseilha”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A dramatic limestone canyon in north Lebanon with a striking Mamluk-era fortress on a lone rock.”},
{“name”: “Douma Village Trails”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “A beautifully preserved mountain village with Ottoman stone houses and vineyard walking routes.”},
{“name”: “Jezzine Forest Walks”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Pine and cedar forests above the famous Bisri waterfall, ideal for peaceful morning hikes.”},
{“name”: “Tyre Coast Nature Reserve”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Lebanon’s only sandy beach nature reserve, nesting ground for loggerhead sea turtles.”},
{“name”: “Laqlouq to Jabal Kneisseh”, “type”: “Hiking”, “difficulty”: “hard”, “description”: “A rugged high-mountain trail across the spine of Mount Lebanon with extreme panoramic views.”},
{“name”: “Cedars of God, Bcharre”, “type”: “Hiking”, “difficulty”: “easy”, “description”: “Walk among the most ancient cedar trees in Lebanon, some over 3,000 years old, near Bcharre.”},
]

def get_quote_of_the_day():
logger.info(”— Picking: Quote of the Day —”)
idx = _daily_index(“quote”, len(_QUOTES))
q = _QUOTES[idx]
logger.info(“Quote: %s”, q[“author”])
return q

def get_song_of_the_day():
logger.info(”— Picking: Guitar Song of the Day —”)
idx = _daily_index(“song”, len(_SONGS))
song = _SONGS[idx]
logger.info(“Song: %s by %s”, song[“title”], song[“artist”])
return song

def get_adventure_of_the_day():
logger.info(”— Picking: Adventure of the Day —”)
idx = _daily_index(“adventure”, len(_ADVENTURES))
adv = _ADVENTURES[idx]
logger.info(“Adventure: %s”, adv[“name”])
return adv

# ── External API fetches ─────────────────────────────────────────────────────

_BOOK_NAMES = {
1: “Genesis”, 2: “Exodus”, 3: “Leviticus”, 4: “Numbers”, 5: “Deuteronomy”,
6: “Joshua”, 7: “Judges”, 8: “Ruth”, 9: “1 Samuel”, 10: “2 Samuel”,
11: “1 Kings”, 12: “2 Kings”, 13: “1 Chronicles”, 14: “2 Chronicles”,
15: “Ezra”, 16: “Nehemiah”, 17: “Esther”, 18: “Job”, 19: “Psalms”,
20: “Proverbs”, 21: “Ecclesiastes”, 22: “Song of Solomon”, 23: “Isaiah”,
24: “Jeremiah”, 25: “Lamentations”, 26: “Ezekiel”, 27: “Daniel”,
28: “Hosea”, 29: “Joel”, 30: “Amos”, 31: “Obadiah”, 32: “Jonah”,
33: “Micah”, 34: “Nahum”, 35: “Habakkuk”, 36: “Zephaniah”, 37: “Haggai”,
38: “Zechariah”, 39: “Malachi”, 40: “Matthew”, 41: “Mark”, 42: “Luke”,
43: “John”, 44: “Acts”, 45: “Romans”, 46: “1 Corinthians”,
47: “2 Corinthians”, 48: “Galatians”, 49: “Ephesians”, 50: “Philippians”,
51: “Colossians”, 52: “1 Thessalonians”, 53: “2 Thessalonians”,
54: “1 Timothy”, 55: “2 Timothy”, 56: “Titus”, 57: “Philemon”,
58: “Hebrews”, 59: “James”, 60: “1 Peter”, 61: “2 Peter”,
62: “1 John”, 63: “2 John”, 64: “3 John”, 65: “Jude”, 66: “Revelation”,
}

def get_verse_of_the_day():
logger.info(”— Fetching: Verse of the Day —”)
try:
data = _fetch_json(“https://bolls.life/get-random-verse/NIV/”)
book_name = _BOOK_NAMES.get(data[“book”], f”Book {data[‘book’]}”)
reference = f”{book_name} {data[‘chapter’]}:{data[‘verse’]}”
text = (
data[“text”]
.replace(”<p>”, “”).replace(”</p>”, “”)
.replace(”<i>”, “”).replace(”</i>”, “”)
.strip()
)
logger.info(“Verse fetched: %s”, reference)
return {“text”: text, “reference”: reference}
except Exception as exc:
logger.error(“Verse fetch failed: %s”, exc)
logger.warning(“FALLBACK triggered for verse”)
return {“text”: “Verse unavailable today.”, “reference”: “—”}

def _weather_label(code):
return {
0: “Clear sky”, 1: “Mainly clear”, 2: “Partly cloudy”, 3: “Overcast”,
45: “Foggy”, 48: “Rime fog”, 51: “Light drizzle”, 53: “Drizzle”,
55: “Dense drizzle”, 61: “Slight rain”, 63: “Rain”, 65: “Heavy rain”,
80: “Rain showers”, 81: “Rain showers”, 82: “Heavy rain showers”,
95: “Thunderstorm”,
}.get(code, “Mixed weather”)

def _weather_emoji(code):
if code == 0: return “☀️”
if code == 1: return “🌤️”
if code == 2: return “⛅”
if code == 3: return “☁️”
if code in (45, 48): return “🌫️”
if code in (51, 53, 55, 61, 63, 65, 80, 81, 82): return “🌧️”
if code == 95: return “⛈️”
return “🌡️”

def get_weather():
logger.info(”— Fetching: Weather (7 days) —”)
lat, lon = 33.8938, 35.5018
url = (
“https://api.open-meteo.com/v1/forecast?”
f”latitude={lat}&longitude={lon}”
“&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum”
“&timezone=Asia%2FBeirut&forecast_days=7”
)
try:
data = _fetch_json(url)
daily = data[“daily”]
days = []
for i in range(7):
code = daily[“weathercode”][i]
days.append({
“date”: daily[“time”][i],
“condition”: _weather_label(code),
“emoji”: _weather_emoji(code),
“temp_max”: round(daily[“temperature_2m_max”][i]),
“temp_min”: round(daily[“temperature_2m_min”][i]),
“rain_mm”: round(daily[“precipitation_sum”][i], 1),
})
logger.info(“Weather fetched: 7 days”)
return {“city”: “Beirut, Lebanon”, “days”: days}
except Exception as exc:
logger.error(“Weather fetch failed: %s”, exc)
logger.warning(“FALLBACK triggered for weather”)
fallback_day = {“date”: “—”, “condition”: “Unavailable”, “emoji”: “🌡️”, “temp_max”: “—”, “temp_min”: “—”, “rain_mm”: “—”}
return {“city”: “Beirut, Lebanon”, “days”: [fallback_day] * 7}

def get_international_news():
logger.info(”— Fetching: International News —”)
api_key = os.getenv(“GNEWS_API_KEY”)
if not api_key:
logger.error(“GNEWS_API_KEY env variable is missing”)
return {“headlines”: [{“title”: “News unavailable (GNEWS_API_KEY not configured).”, “source”: “—”, “url”: “”}]}
url = f”https://gnews.io/api/v4/top-headlines?category=general&lang=en&max=3&apikey={api_key}”
try:
data = _fetch_json(url)
articles = data.get(“articles”, [])
if not articles:
raise ValueError(“No articles returned from GNews API”)
headlines = [
{“title”: a[“title”].strip(), “source”: a.get(“source”, {}).get(“name”, “Unknown”).strip(), “url”: a.get(“url”, “”).strip()}
for a in articles[:3]
]
logger.info(“News fetched: %d headlines”, len(headlines))
return {“headlines”: headlines}
except Exception as exc:
logger.error(“News fetch failed: %s”, exc)
logger.warning(“FALLBACK triggered for news”)
return {“headlines”: [{“title”: “News unavailable.”, “source”: “—”, “url”: “”}]}

def get_fun_fact():
logger.info(”— Fetching: Fun Fact —”)
try:
data = _fetch_json(“https://uselessfacts.jsph.pl/api/v2/facts/random?language=en”)
logger.info(“Fun fact fetched successfully”)
return data[“text”].strip()
except Exception as exc:
logger.error(“Fun fact fetch failed: %s”, exc)
logger.warning(“FALLBACK triggered for fun fact”)
return “Fun fact unavailable today.”

def generate_daily_content():
return {
“verse”: get_verse_of_the_day(),
“weather”: get_weather(),
“news”: get_international_news(),
“fun_fact”: get_fun_fact(),
“quote”: get_quote_of_the_day(),
“song”: get_song_of_the_day(),
“adventure”: get_adventure_of_the_day(),
}
