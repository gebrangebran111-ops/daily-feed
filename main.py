from data.quotes import get_quote
from data.quotes import QUOTES
from data.songs import get_song
from data.songs import SONGS
from data.songs import DIFFICULTY_ORDER as SONG_DIFFICULTY_ORDER
from data.locations import get_location
from data.locations import LOCATIONS
from data.locations import DIFFICULTY_ORDER as LOCATION_DIFFICULTY_ORDER
from services.email_service import send_email
from services.used_items_service import load_used_items
from services.used_items_service import save_used_items
from services.used_items_service import reset_if_all_used


def build_daily_message():
    used_items = load_used_items()
    used_items = reset_if_all_used(used_items, len(QUOTES), len(SONGS), len(LOCATIONS))

    quote = get_quote(used_items["quotes"])
    song_difficulty = SONG_DIFFICULTY_ORDER[
        used_items["song_difficulty_index"] % len(SONG_DIFFICULTY_ORDER)
    ]
    location_difficulty = LOCATION_DIFFICULTY_ORDER[
        used_items["location_difficulty_index"] % len(LOCATION_DIFFICULTY_ORDER)
    ]

    song = get_song(
        used_items["songs"],
        target_difficulty=song_difficulty,
        excluded_artist=used_items.get("last_song_artist"),
    )
    location = get_location(
        used_items["locations"],
        target_difficulty=location_difficulty,
        excluded_type=used_items.get("last_location_type"),
    )

    used_items["quotes"].append(quote)
    used_items["songs"].append(f"{song['title']}::{song['artist']}")
    used_items["locations"].append(location["name"])
    used_items["song_difficulty_index"] += 1
    used_items["location_difficulty_index"] += 1
    used_items["last_song_artist"] = song["artist"]
    used_items["last_location_type"] = location["type"]
    save_used_items(used_items)

    lines = [
        "DAILY FEED",
        "Your personal morning boost",
        "",
        "----------------------------------------------",
        "💬 QUOTE",
        "----------------------------------------------",
        "",
        f"\"{quote}\"",
        "",
        "----------------------------------------------",
        "🎸 GUITAR",
        "----------------------------------------------",
        "",
        f"Song       : {song['title']}",
        f"Artist     : {song['artist']}",
        f"Difficulty : {song['difficulty'].title()}",
        f"Chords     : {song['chords']}",
        "",
        "----------------------------------------------",
        "🏕️ ADVENTURE (LEBANON)",
        "----------------------------------------------",
        "",
        f"Spot       : {location['name']}",
        f"Type       : {location['type']} ({location['difficulty'].title()})",
        f"Description: {location['description']}",
        "",
        "Tip: Small steps daily create big results.",
        "",
        "Have a strong day! 🌞",
    ]

    html = f"""
<html>
  <body style="margin:0;padding:0;background:#f4f7fb;font-family:Arial,sans-serif;color:#1f2937;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="padding:24px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="640" cellspacing="0" cellpadding="0" style="background:#ffffff;border-radius:14px;overflow:hidden;border:1px solid #e5e7eb;">
            <tr>
              <td style="padding:24px 28px;background:#0f172a;color:#ffffff;">
                <h1 style="margin:0;font-size:24px;">Daily Feed</h1>
                <p style="margin:8px 0 0 0;color:#cbd5e1;">Your personal morning boost</p>
              </td>
            </tr>
            <tr>
              <td style="padding:22px 28px;">
                <h2 style="margin:0 0 10px 0;font-size:18px;">💬 Quote</h2>
                <p style="margin:0 0 18px 0;line-height:1.7;">"{quote}"</p>

                <h2 style="margin:0 0 10px 0;font-size:18px;">🎸 Guitar</h2>
                <p style="margin:0 0 6px 0;"><strong>Song:</strong> {song["title"]}</p>
                <p style="margin:0 0 6px 0;"><strong>Artist:</strong> {song["artist"]}</p>
                <p style="margin:0 0 6px 0;"><strong>Difficulty:</strong> {song["difficulty"].title()}</p>
                <p style="margin:0 0 18px 0;"><strong>Chords:</strong> {song["chords"]}</p>

                <h2 style="margin:0 0 10px 0;font-size:18px;">🏕️ Adventure (Lebanon)</h2>
                <p style="margin:0 0 6px 0;"><strong>Spot:</strong> {location["name"]}</p>
                <p style="margin:0 0 6px 0;"><strong>Type:</strong> {location["type"]} ({location["difficulty"].title()})</p>
                <p style="margin:0 0 18px 0;"><strong>Description:</strong> {location["description"]}</p>

                <div style="padding:12px 14px;border:1px solid #e5e7eb;border-radius:8px;background:#f8fafc;">
                  <p style="margin:0;">Tip: Small steps daily create big results.</p>
                </div>
              </td>
            </tr>
            <tr>
              <td style="padding:14px 28px;background:#f8fafc;color:#64748b;font-size:12px;">
                Have a strong day! 🌞
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
""".strip()

    return {"text": "\n".join(lines), "html": html}


if __name__ == "__main__":
    content = build_daily_message()
    print(content["text"])
    send_email(content)
    print("\nEmail sent successfully.")
