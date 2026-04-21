import os
from datetime import datetime
from zoneinfo import ZoneInfo

from services.email_service import send_email
from services.daily_content_service import generate_daily_content


def should_send_now():
    if os.getenv("DAILY_FEED_FORCE_SEND", "").lower() in {"1", "true", "yes"}:
        return True
    beirut_now = datetime.now(ZoneInfo("Asia/Beirut"))
    return beirut_now.hour == 7


def build_daily_message():
    daily = generate_daily_content()
    verse = daily["verse"]
    weather = daily["weather"]
    news = daily["news"]
    fun_fact = daily["fun_fact"]
    quote = daily["quote"]
    today_weather = weather["days"][0]
    next_weather = weather["days"][1]

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
        f"{news['title']}",
        f"Source: {news['source']}",
        f"Link  : {news['url'] or 'Not available'}",
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
                <h2 style="margin:0 0 10px 0;font-size:18px;">📖 Verse of the Day</h2>
                <p style="margin:0 0 4px 0;line-height:1.7;">"{verse["text"]}"</p>
                <p style="margin:0 0 18px 0;color:#64748b;"><em>{verse["reference"]}</em></p>

                <h2 style="margin:0 0 10px 0;font-size:18px;">🌤️ Weather (Beirut)</h2>
                <p style="margin:0 0 6px 0;"><strong>Today:</strong> {today_weather["condition"]}, {today_weather["temp_min"]}C to {today_weather["temp_max"]}C, rain {today_weather["rain_mm"]} mm</p>
                <p style="margin:0 0 18px 0;"><strong>Tomorrow:</strong> {next_weather["condition"]}, {next_weather["temp_min"]}C to {next_weather["temp_max"]}C, rain {next_weather["rain_mm"]} mm</p>

                <h2 style="margin:0 0 10px 0;font-size:18px;">🗞️ Big International News</h2>
                <p style="margin:0 0 6px 0;"><strong>Headline:</strong> {news["title"]}</p>
                <p style="margin:0 0 6px 0;"><strong>Source:</strong> {news["source"]}</p>
                <p style="margin:0 0 18px 0;"><strong>Link:</strong> {news["url"] or "Not available"}</p>

                <h2 style="margin:0 0 10px 0;font-size:18px;">🧠 Fun Fact of the Day</h2>
                <p style="margin:0 0 18px 0;line-height:1.7;">{fun_fact}</p>

                <h2 style="margin:0 0 10px 0;font-size:18px;">💬 Quote of the Day</h2>
                <p style="margin:0 0 4px 0;line-height:1.7;">"{quote["text"]}"</p>
                <p style="margin:0 0 18px 0;color:#64748b;"><em>- {quote["author"]}</em></p>

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
