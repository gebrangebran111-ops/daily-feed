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
    today = weather["days"][0]
    tomorrow = weather["days"][1]

    # ── Plain text version ──────────────────────────────────────────────────
    news_lines = []
    for item in news["headlines"]:
        line = f"  • {item['title']} ({item['source']})"
        if item.get("url"):
            line += f"\n    {item['url']}"
        news_lines.append(line)

    lines = [
        "DAILY FEED — Your morning boost",
        "=" * 48,
        "",
        "📖  VERSE OF THE DAY",
        f'"{verse["text"]}"',
        f"    — {verse['reference']}",
        "",
        "🌤️  WEATHER · BEIRUT",
        f"  Today     {today['emoji']}  {today['condition']}, {today['temp_min']}–{today['temp_max']}°C, rain {today['rain_mm']} mm",
        f"  Tomorrow  {tomorrow['emoji']}  {tomorrow['condition']}, {tomorrow['temp_min']}–{tomorrow['temp_max']}°C, rain {tomorrow['rain_mm']} mm",
        "",
        "🗞️  TOP INTERNATIONAL NEWS",
        *news_lines,
        "",
        "🧠  FUN FACT",
        f"  {fun_fact}",
        "",
        "💬  QUOTE OF THE DAY",
        f'"{quote["text"]}"',
        f"    — {quote['author']}",
        "",
        "🎸  GUITAR PICK",
        f"  Song       {song['title']}",
        f"  Artist     {song['artist']}",
        f"  Difficulty {song['difficulty'].title()}",
        f"  Chords     {song['chords']}",
        "",
        "🏕️  LEBANON ADVENTURE PICK",
        f"  {adventure['name']} ({adventure['type']} · {adventure['difficulty'].title()})",
        f"  {adventure['description']}",
        "",
        "Have a strong day! 🌞",
    ]

    # ── HTML version ────────────────────────────────────────────────────────
    news_html_items = ""
    for item in news["headlines"]:
        if item.get("url"):
            title_html = f'<a href="{item["url"]}" style="color:#1a1a2e;text-decoration:none;font-weight:600;" target="_blank">{item["title"]}</a>'
        else:
            title_html = f'<span style="font-weight:600;">{item["title"]}</span>'
        news_html_items += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #f0f0f0;">
            <div style="font-size:14px;line-height:1.5;color:#1a1a2e;">{title_html}</div>
            <div style="font-size:12px;color:#888;margin-top:3px;">{item['source']}</div>
          </td>
        </tr>"""

    difficulty_colors = {"easy": "#22c55e", "medium": "#f59e0b", "hard": "#ef4444"}
    song_diff_color = difficulty_colors.get(song["difficulty"].lower(), "#888")
    adv_diff_color = difficulty_colors.get(adventure["difficulty"].lower(), "#888")

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Feed</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background-color: #f4f1ec; font-family: 'DM Sans', Arial, sans-serif; -webkit-text-size-adjust: 100%; }}
  .wrapper {{ background:#f4f1ec; padding:24px 16px; }}
  .card {{ background:#ffffff; border-radius:20px; overflow:hidden; max-width:600px; margin:0 auto; box-shadow:0 4px 24px rgba(0,0,0,0.08); }}
  .header {{ background:#1a1a2e; padding:28px 28px 24px; }}
  .header-title {{ font-family:'DM Serif Display', Georgia, serif; font-size:30px; color:#ffffff; letter-spacing:-0.5px; margin-bottom:4px; }}
  .header-sub {{ font-size:13px; color:#8888aa; font-weight:300; letter-spacing:0.5px; text-transform:uppercase; }}
  .header-date {{ font-size:12px; color:#5555aa; margin-top:8px; font-weight:400; }}
  .body {{ padding:20px 20px 24px; }}
  .section {{ background:#fafafa; border:1px solid #efefef; border-radius:14px; padding:18px; margin-bottom:14px; }}
  .section-alt {{ background:#ffffff; }}
  .section-accent {{ background:#1a1a2e; border-color:#1a1a2e; }}
  .label {{ font-size:10px; font-weight:600; letter-spacing:1.5px; text-transform:uppercase; color:#aaa; margin-bottom:10px; display:flex; align-items:center; gap:6px; }}
  .label-accent {{ color:#5555aa; }}
  .verse-text {{ font-family:'DM Serif Display', Georgia, serif; font-size:17px; line-height:1.65; color:#1a1a2e; font-style:italic; margin-bottom:8px; }}
  .verse-ref {{ font-size:12px; color:#888; font-weight:500; }}
  .weather-row {{ display:flex; gap:10px; }}
  .weather-day {{ flex:1; background:#f0ede8; border-radius:10px; padding:12px; text-align:center; }}
  .weather-day-label {{ font-size:10px; font-weight:600; color:#888; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px; }}
  .weather-emoji {{ font-size:26px; margin-bottom:4px; }}
  .weather-condition {{ font-size:12px; color:#444; margin-bottom:4px; font-weight:500; }}
  .weather-temp {{ font-size:14px; font-weight:600; color:#1a1a2e; }}
  .weather-rain {{ font-size:11px; color:#888; margin-top:2px; }}
  .quote-text {{ font-family:'DM Serif Display', Georgia, serif; font-size:16px; line-height:1.7; color:#ffffff; font-style:italic; margin-bottom:8px; }}
  .quote-author {{ font-size:12px; color:#8888aa; font-weight:500; }}
  .fact-text {{ font-size:14px; line-height:1.6; color:#333; }}
  .song-grid {{ display:grid; grid-template-columns:auto 1fr; gap:5px 12px; }}
  .song-label {{ font-size:11px; color:#aaa; font-weight:600; text-transform:uppercase; letter-spacing:0.8px; padding-top:1px; }}
  .song-value {{ font-size:14px; color:#1a1a2e; font-weight:500; line-height:1.4; }}
  .badge {{ display:inline-block; font-size:10px; font-weight:700; letter-spacing:0.8px; text-transform:uppercase; padding:2px 8px; border-radius:20px; color:#fff; }}
  .chords {{ font-family:monospace; font-size:13px; color:#1a1a2e; background:#f0ede8; padding:6px 10px; border-radius:8px; margin-top:8px; display:block; letter-spacing:0.3px; }}
  .adv-name {{ font-size:16px; font-weight:600; color:#1a1a2e; margin-bottom:4px; }}
  .adv-meta {{ font-size:12px; color:#888; margin-bottom:8px; }}
  .adv-desc {{ font-size:14px; line-height:1.6; color:#444; }}
  .footer {{ text-align:center; padding:16px 20px 20px; color:#aaa; font-size:12px; }}
  @media only screen and (max-width:480px) {{
    .wrapper {{ padding:12px 8px; }}
    .header {{ padding:22px 18px 18px; }}
    .header-title {{ font-size:24px; }}
    .body {{ padding:14px 14px 18px; }}
    .section {{ padding:14px; }}
    .verse-text {{ font-size:15px; }}
    .weather-condition {{ font-size:11px; }}
    .song-grid {{ grid-template-columns:1fr; gap:4px; }}
    .song-label {{ display:none; }}
  }}
</style>
</head>
<body>
<div class="wrapper">
<div class="card">

  <!-- HEADER -->
  <div class="header">
    <div class="header-title">Daily Feed</div>
    <div class="header-sub">Your morning boost</div>
    <div class="header-date">{datetime.now(ZoneInfo("Asia/Beirut")).strftime("%A, %B %-d, %Y")} &nbsp;·&nbsp; Beirut</div>
  </div>

  <div class="body">

    <!-- VERSE -->
    <div class="section">
      <div class="label">📖 &nbsp;Verse of the Day</div>
      <div class="verse-text">"{verse["text"]}"</div>
      <div class="verse-ref">{verse["reference"]}</div>
    </div>

    <!-- WEATHER -->
    <div class="section section-alt">
      <div class="label">🌤️ &nbsp;Weather · Beirut</div>
      <div class="weather-row">
        <div class="weather-day">
          <div class="weather-day-label">Today</div>
          <div class="weather-emoji">{today["emoji"]}</div>
          <div class="weather-condition">{today["condition"]}</div>
          <div class="weather-temp">{today["temp_min"]}° – {today["temp_max"]}°C</div>
          <div class="weather-rain">🌧 {today["rain_mm"]} mm</div>
        </div>
        <div class="weather-day">
          <div class="weather-day-label">Tomorrow</div>
          <div class="weather-emoji">{tomorrow["emoji"]}</div>
          <div class="weather-condition">{tomorrow["condition"]}</div>
          <div class="weather-temp">{tomorrow["temp_min"]}° – {tomorrow["temp_max"]}°C</div>
          <div class="weather-rain">🌧 {tomorrow["rain_mm"]} mm</div>
        </div>
      </div>
    </div>

    <!-- NEWS -->
    <div class="section">
      <div class="label">🗞️ &nbsp;Top International News</div>
      <table width="100%" cellspacing="0" cellpadding="0">
        {news_html_items}
      </table>
    </div>

    <!-- FUN FACT -->
    <div class="section section-alt">
      <div class="label">🧠 &nbsp;Fun Fact</div>
      <div class="fact-text">{fun_fact}</div>
    </div>

    <!-- QUOTE -->
    <div class="section section-accent">
      <div class="label label-accent">💬 &nbsp;Quote of the Day</div>
      <div class="quote-text">"{quote["text"]}"</div>
      <div class="quote-author">— {quote["author"]}</div>
    </div>

    <!-- GUITAR PICK -->
    <div class="section section-alt">
      <div class="label">🎸 &nbsp;Guitar Pick</div>
      <div class="song-grid">
        <div class="song-label">Song</div>
        <div class="song-value" style="font-size:16px;font-weight:700;">{song["title"]}</div>
        <div class="song-label">Artist</div>
        <div class="song-value" style="color:#555;">{song["artist"]}</div>
        <div class="song-label">Level</div>
        <div class="song-value"><span class="badge" style="background:{song_diff_color};">{song["difficulty"].title()}</span></div>
      </div>
      <span class="chords">{song["chords"]}</span>
    </div>

    <!-- ADVENTURE PICK -->
    <div class="section">
      <div class="label">🏕️ &nbsp;Lebanon Adventure Pick</div>
      <div class="adv-name">{adventure["name"]}</div>
      <div class="adv-meta">{adventure["type"]} &nbsp;·&nbsp; <span class="badge" style="background:{adv_diff_color};">{adventure["difficulty"].title()}</span></div>
      <div class="adv-desc">{adventure["description"]}</div>
    </div>

  </div><!-- /body -->

  <div class="footer">Have a strong day! 🌞</div>

</div><!-- /card -->
</div><!-- /wrapper -->
</body>
</html>"""

    return {"text": "\n".join(lines), "html": html}


if __name__ == "__main__":
    if not should_send_now():
        logger.info("Skipped: not 7 AM Beirut time")
        raise SystemExit(0)
    content = build_daily_message()
    logger.info("Daily content built successfully")
    print(content["text"])
    send_email(content)
    logger.info("Email sent successfully")
