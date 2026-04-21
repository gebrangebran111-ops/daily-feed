import os
from datetime import datetime
from zoneinfo import ZoneInfo

from services.email_service import send_email
from services.openai_service import generate_daily_content


def _fallback_daily_content():
    return {
        "quote": "Small progress every day adds up to big results.",
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
        },
    }


def should_send_now():
    if os.getenv("DAILY_FEED_FORCE_SEND", "").lower() in {"1", "true", "yes"}:
        return True
    beirut_now = datetime.now(ZoneInfo("Asia/Beirut"))
    return beirut_now.hour == 7


def build_daily_message():
    try:
        daily = generate_daily_content()
    except Exception:
        # Keep the daily email flowing even if OpenAI is temporarily rate-limited.
        daily = _fallback_daily_content()
    quote = daily["quote"]
    song = daily["song"]
    location = daily["adventure"]

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
    if not should_send_now():
        print("Skipped: not 7 AM Beirut time.")
        raise SystemExit(0)
    content = build_daily_message()
    print(content["text"])
    send_email(content)
    print("\nEmail sent successfully.")
