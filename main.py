from data.quotes import get_quote
from data.quotes import QUOTES
from data.songs import get_song
from data.songs import SONGS
from data.locations import get_location
from data.locations import LOCATIONS
from services.email_service import send_email
from services.used_items_service import load_used_items
from services.used_items_service import save_used_items
from services.used_items_service import reset_if_all_used


def build_daily_message():
    used_items = load_used_items()
    used_items = reset_if_all_used(used_items, len(QUOTES), len(SONGS), len(LOCATIONS))

    quote = get_quote(used_items["quotes"])
    song = get_song(used_items["songs"])
    location = get_location(used_items["locations"])

    used_items["quotes"].append(quote)
    used_items["songs"].append(f"{song['title']}::{song['artist']}")
    used_items["locations"].append(location["name"])
    save_used_items(used_items)

    lines = [
        "",
        "==================================================",
        "                DAILY FEED NEWSLETTER             ",
        "==================================================",
        "",
        "💬 QUOTE OF THE DAY",
        "",
        f"\"{quote}\"",
        "",
        "--------------------------------------------------",
        "",
        "🎸 GUITAR SONG PICK",
        "",
        f"Title : {song['title']}",
        f"Artist: {song['artist']}",
        f"Chords: {song['chords']}",
        "",
        "--------------------------------------------------",
        "",
        "🏕️ HIKING / CAMPING SPOT",
        "",
        f"Name       : {location['name']}",
        f"Type       : {location['type']}",
        f"Description: {location['description']}",
        "",
        "--------------------------------------------------",
        "",
        "✨ Have a great day and keep going!",
        "☀️ See you in tomorrow's Daily Feed.",
        "",
        "==================================================",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    content = build_daily_message()
    print(content)
    send_email(content)
    print("\nEmail sent successfully.")