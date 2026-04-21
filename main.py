import os
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from services.email_service import send_email
from services.daily_content_service import generate_daily_content

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("daily_feed.main")


def should_send_now():
    if os.getenv("DAILY_FEED_FORCE_SEND", "").lower() in {"1", "true", "yes"}:
        return True
    beirut_now = datetime.now(ZoneInfo("Asia/Beirut"))
    return beirut_now.hour == 7


def build_daily_message():
    logger.info("Building daily message")
    daily = generate_daily_content()
    verse = daily["verse"]
    weather = daily["weather"]
    news = daily["news"]
    fun_fact = daily["fun_fact"]
    quote = daily["quote"]
    song = daily["song"]
    adventure = daily["adventure"]
    today_weather = weather["days"][0]
    next_weather = weather["days"][1]

    news_lines = [f"- {item['title']} ({item['source']})" for item in news["headlines"]]
    news_html = "".join(
        [
            (
                '<li style="margin:0 0 8px 0;line-height:1.5;">'
                f'{item["title"]} <span style="color:#64748b;">({item["source"]})</span>'
                "</li>"
            )
            for item in news["headlines"]
        ]
    )

    lines = [
        "DAILY FEED",
        "Your personal morning boost",
        "",
        "----------------------------------------------",
        "📖 VERSE OF THE DAY",
        "----------------------------------------------",
        "",
        f"\"{verse['text']}\"",
        f"- {verse['reference']}",
        "",
        "----------------------------------------------",
        "🌤️ WEATHER (BEIRUT)",
        "----------------------------------------------",
        "",
        f"Today    : {today_weather['condition']}, {today_weather['temp_min']}C to {today_weather['temp_max']}C, rain {today_weather['rain_mm']} mm",
        f"Tomorrow : {next_weather['condition']}, {next_weather['temp_min']}C to {next_weather['temp_max']}C, rain {next_weather['rain_mm']} mm",
        "",
        "----------------------------------------------",
        "🗞️ BIG INTERNATIONAL NEWS",
        "----------------------------------------------",
        "",
        *news_lines,
        "",
        "----------------------------------------------",
        "🧠 FUN FACT OF THE DAY",
        "----------------------------------------------",
        "",
        fun_fact,
        "",
        "----------------------------------------------",
        "💬 QUOTE OF THE DAY",
        "----------------------------------------------",
        "",
        f"\"{quote['text']}\"",
        f"- {quote['author']}",
        "",
        "----------------------------------------------",
        "🎸 AI GUITAR SONG PICK",
        "----------------------------------------------",
        "",
        f"Song       : {song['title']}",
        f"Artist     : {song['artist']}",
        f"Difficulty : {song['difficulty'].title()}",
        f"Chords     : {song['chords']}",
        "",
        "----------------------------------------------",
        "🏕️ AI ADVENTURE PICK (LEBANON)",
        "----------------------------------------------",
        "",
        f"Spot       : {adventure['name']}",
        f"Type       : {adventure['type']} ({adventure['difficulty'].title()})",
        f"Description: {adventure['description']}",
        "",
        "Have a strong day! 🌞",
    ]

    html = f"""
<html>
  <body style="margin:0;padding:0;background:#eef2f7;font-family:Arial,sans-serif;color:#1f2937;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="padding:32px 0;">
      <tr>
        <td align="center">
          <table role="presentation" width="680" cellspacing="0" cellpadding="0" style="background:#ffffff;border-radius:16px;overflow:hidden;border:1px solid #dbe3ef;">
            <tr>
              <td style="padding:26px 30px;background:#0f172a;color:#ffffff;text-align:left;">
                <h1 style="margin:0;font-size:26px;letter-spacing:0.3px;">Daily Feed</h1>
                <p style="margin:8px 0 0 0;color:#cbd5e1;">Your personal morning newsletter</p>
              </td>
            </tr>
            <tr>
              <td style="padding:24px 26px 16px 26px;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#f8fafc;margin:0 0 14px 0;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">📖 Verse of the Day</h2>
                    <p style="margin:0 0 4px 0;line-height:1.7;">"{verse["text"]}"</p>
                    <p style="margin:0;color:#64748b;"><em>{verse["reference"]}</em></p>
                  </td></tr>
                </table>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#ffffff;margin:0 0 14px 0;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">🌤️ Weather (Beirut)</h2>
                    <p style="margin:0 0 6px 0;"><strong>Today:</strong> {today_weather["condition"]}, {today_weather["temp_min"]}C to {today_weather["temp_max"]}C, rain {today_weather["rain_mm"]} mm</p>
                    <p style="margin:0;"><strong>Tomorrow:</strong> {next_weather["condition"]}, {next_weather["temp_min"]}C to {next_weather["temp_max"]}C, rain {next_weather["rain_mm"]} mm</p>
                  </td></tr>
                </table>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#ffffff;margin:0 0 14px 0;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">🗞️ Big International News</h2>
                    <ul style="margin:0;padding-left:18px;">{news_html}</ul>
                  </td></tr>
                </table>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#ffffff;margin:0 0 14px 0;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">🧠 Fun Fact of the Day</h2>
                    <p style="margin:0;line-height:1.7;">{fun_fact}</p>
                  </td></tr>
                </table>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#ffffff;margin:0 0 14px 0;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">💬 Quote of the Day</h2>
                    <p style="margin:0 0 4px 0;line-height:1.7;">"{quote["text"]}"</p>
                    <p style="margin:0;color:#64748b;"><em>- {quote["author"]}</em></p>
                  </td></tr>
                </table>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#ffffff;margin:0 0 14px 0;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">🎸 AI Guitar Song Pick</h2>
                    <p style="margin:0 0 6px 0;"><strong>Song:</strong> {song["title"]}</p>
                    <p style="margin:0 0 6px 0;"><strong>Artist:</strong> {song["artist"]}</p>
                    <p style="margin:0 0 6px 0;"><strong>Difficulty:</strong> {song["difficulty"].title()}</p>
                    <p style="margin:0;"><strong>Chords:</strong> {song["chords"]}</p>
                  </td></tr>
                </table>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="border:1px solid #e5e7eb;border-radius:12px;background:#ffffff;">
                  <tr><td style="padding:14px 16px;">
                    <h2 style="margin:0 0 8px 0;font-size:18px;">🏕️ AI Location Pick (Lebanon)</h2>
                    <p style="margin:0 0 6px 0;"><strong>Spot:</strong> {adventure["name"]}</p>
                    <p style="margin:0 0 6px 0;"><strong>Type:</strong> {adventure["type"]} ({adventure["difficulty"].title()})</p>
                    <p style="margin:0;"><strong>Description:</strong> {adventure["description"]}</p>
                  </td></tr>
                </table>
                
                <div style="padding:14px 2px 0 2px;">
                  <p style="margin:0;color:#64748b;">Have a strong day! 🌞</p>
                </div>
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
        logger.info("Skipped send: not 7 AM Beirut time")
        raise SystemExit(0)
    content = build_daily_message()
    logger.info("Daily content built successfully")
    print(content["text"])
    send_email(content)
    logger.info("Email sent successfully")
