from data.quotes import get_quote
from data.songs import get_song
from data.locations import get_location
from services.email_service import send_email


def build_daily_message():
    quote = get_quote()
    song = get_song()
    location = get_location()

    lines = [
        "========================================",
        "        DAILY INSPIRATION FEED",
        "========================================",
        "",
        "💬 QUOTE OF THE DAY",
        f"\"{quote}\"",
        "",
        "----------------------------------------",
        "",
        "🎸 GUITAR SONG PICK",
        f"Title : {song['title']}",
        f"Artist: {song['artist']}",
        f"Chords: {song['chords']}",
        "",
        "----------------------------------------",
        "",
        "🏕️ HIKING / CAMPING LOCATION",
        f"Name       : {location['name']}",
        f"Type       : {location['type']}",
        f"Description: {location['description']}",
        "",
        "========================================",
        "Have a great day! 🌞",
        "========================================",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    content = build_daily_message()
    print(content)
    send_email(content)
    print("\nEmail sent successfully.")