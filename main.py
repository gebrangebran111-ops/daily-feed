import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from services.daily_content_service import generate_daily_content
from services.email_service import send_email

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("daily_feed.main")


def build_daily_message():
    logger.info("Building daily message")
    daily = generate_daily_content()
    verse   = daily["verse"]
    weather = daily["weather"]
    news    = daily["news"]
    fun_fact = daily["fun_fact"]
    quote   = daily["quote"]
    song    = daily["song"]
    adventure = daily["adventure"]

    days = weather["days"]  # 7 days

    # ── Plain text ───────────────────────────────────────────────────────────
    day_labels = ["Today", "Tomorrow", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"]
    weather_lines = []
    for i, d in enumerate(days):
        label = day_labels[i] if i < len(day_labels) else d["date"]
        weather_lines.append(
            f"  {label:<9} {d['emoji']}  {d['condition']}, {d['temp_min']}–{d['temp_max']}°C, rain {d['rain_mm']} mm"
        )

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
        "🌤️  WEATHER · BEIRUT (7 DAYS)",
        *weather_lines,
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

    # ── HTML ─────────────────────────────────────────────────────────────────
    news_html_items = ""
    for item in news["headlines"]:
        if item.get("url"):
            title_html = (
                f'<a href="{item["url"]}" style="color:#1a1a2e;text-decoration:none;'
                f'font-weight:600;" target="_blank">{item["title"]}</a>'
            )
        else:
            title_html = f'<span style="font-weight:600;">{item["title"]}</span>'
        news_html_items += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #f0f0f0;">
            <div style="font-size:14px;line-height:1.5;color:#1a1a2e;">{title_html}</div>
            <div style="font-size:12px;color:#888;margin-top:3px;">{item['source']}</div>
          </td>
        </tr>"""

    # 7-day weather grid — first day larger, rest compact
    today = days[0]
    rest_days  = days[1:]
    short_labels = ["Mon", "Tue", "Wed", "Thu", "Thu", "Fri", "Sat", "Sun"]

    from datetime import date, timedelta
    base = date.today()
    day_name_map = {0:"Mon",1:"Tue",2:"Wed",3:"Thu",4:"Fri",5:"Sat",6:"Sun"}

    weather_today_html = f"""
    <table width="100%" cellspacing="0" cellpadding="0" style="margin-bottom:10px;">
      <tr>
        <td style="background:#1a1a2e;border-radius:12px;padding:14px 16px;text-align:center;width:48%;vertical-align:middle;">
          <div style="font-size:10px;font-weight:700;color:#8888aa;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;">TODAY</div>
          <div style="font-size:36px;line-height:1;">{today['emoji']}</div>
          <div style="font-size:13px;color:#ccc;margin:6px 0 4px;">{today['condition']}</div>
          <div style="font-size:20px;font-weight:700;color:#fff;">{today['temp_min']}°–{today['temp_max']}°C</div>
          <div style="font-size:11px;color:#8888aa;margin-top:4px;">🌧 {today['rain_mm']} mm</div>
        </td>
        <td width="4%"></td>
        <td style="background:#f0ede8;border-radius:12px;padding:14px 16px;text-align:center;width:48%;vertical-align:middle;">
          <div style="font-size:10px;font-weight:700;color:#aaa;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:6px;">TOMORROW</div>
          <div style="font-size:36px;line-height:1;">{days[1]['emoji']}</div>
          <div style="font-size:13px;color:#555;margin:6px 0 4px;">{days[1]['condition']}</div>
          <div style="font-size:20px;font-weight:700;color:#1a1a2e;">{days[1]['temp_min']}°–{days[1]['temp_max']}°C</div>
          <div style="font-size:11px;color:#aaa;margin-top:4px;">🌧 {days[1]['rain_mm']} mm</div>
        </td>
      </tr>
    </table>"""

    # Days 3–7 as a compact row of 5
    compact_cells = ""
    for i in range(2, 7):
        d = days[i]
        weekday_name = day_name_map[(base + timedelta(days=i)).weekday()]
        compact_cells += f"""
        <td style="text-align:center;padding:10px 4px;background:#fafafa;border-radius:10px;width:19%;">
          <div style="font-size:10px;font-weight:700;color:#aaa;letter-spacing:1px;text-transform:uppercase;">{weekday_name}</div>
          <div style="font-size:22px;margin:4px 0;">{d['emoji']}</div>
          <div style="font-size:12px;font-weight:600;color:#1a1a2e;">{d['temp_max']}°</div>
          <div style="font-size:11px;color:#aaa;">{d['temp_min']}°</div>
        </td>
        <td width="1%"></td>"""

    weather_compact_html = f"""
    <table width="100%" cellspacing="0" cellpadding="0">
      <tr>{compact_cells}</tr>
    </table>"""

    diff_color = {"easy": "#22c55e", "medium": "#f59e0b", "hard": "#ef4444"}
    song_dc = diff_color.get(song["difficulty"].lower(), "#888")
    adv_dc  = diff_color.get(adventure["difficulty"].lower(), "#888")

    now_beirut = datetime.now(ZoneInfo("Asia/Beirut"))

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily Feed</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap');
  *{{box-sizing:border-box;margin:0;padding:0;}}
  body{{background:#f4f1ec;font-family:'DM Sans',Arial,sans-serif;-webkit-text-size-adjust:100%;}}
  .wrapper{{background:#f4f1ec;padding:24px 16px;}}
  .card{{background:#fff;border-radius:20px;overflow:hidden;max-width:600px;margin:0 auto;box-shadow:0 4px 32px rgba(0,0,0,0.10);}}
  .header{{background:#1a1a2e;padding:28px 28px 22px;}}
  .header-title{{font-family:'DM Serif Display',Georgia,serif;font-size:30px;color:#fff;letter-spacing:-0.5px;margin-bottom:4px;}}
  .header-sub{{font-size:12px;color:#8888aa;font-weight:300;letter-spacing:1px;text-transform:uppercase;}}
  .header-date{{font-size:12px;color:#6666bb;margin-top:8px;}}
  .body{{padding:20px 20px 24px;}}
  .section{{background:#fafafa;border:1px solid #efefef;border-radius:14px;padding:18px;margin-bottom:14px;}}
  .section-white{{background:#fff;}}
  .section-dark{{background:#1a1a2e;border-color:#1a1a2e;}}
  .label{{font-size:10px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#bbb;margin-bottom:12px;}}
  .label-light{{color:#6666bb;}}
  .serif{{font-family:'DM Serif Display',Georgia,serif;}}
  .verse-text{{font-family:'DM Serif Display',Georgia,serif;font-size:16px;line-height:1.7;color:#1a1a2e;font-style:italic;margin-bottom:8px;}}
  .verse-ref{{font-size:12px;color:#aaa;font-weight:500;}}
  .quote-text{{font-family:'DM Serif Display',Georgia,serif;font-size:16px;line-height:1.7;color:#fff;font-style:italic;margin-bottom:8px;}}
  .quote-author{{font-size:12px;color:#8888aa;}}
  .fact-text{{font-size:14px;line-height:1.6;color:#333;}}
  .badge{{display:inline-block;font-size:10px;font-weight:700;letter-spacing:0.8px;text-transform:uppercase;padding:3px 9px;border-radius:20px;color:#fff;}}
  .chords{{font-family:monospace;font-size:13px;color:#1a1a2e;background:#f0ede8;padding:7px 11px;border-radius:8px;margin-top:10px;display:block;letter-spacing:0.3px;}}
  .footer{{text-align:center;padding:14px 20px 20px;color:#bbb;font-size:12px;}}
  @media only screen and (max-width:500px){{
    .wrapper{{padding:10px 6px;}}
    .header{{padding:20px 16px 16px;}}
    .header-title{{font-size:24px;}}
    .body{{padding:12px 12px 16px;}}
    .section{{padding:14px;}}
    .verse-text{{font-size:15px;}}
  }}
</style>
</head>
<body>
<div class="wrapper">
<div class="card">

  <div class="header">
    <div class="header-title">Daily Feed</div>
    <div class="header-sub">Your morning boost</div>
    <div class="header-date">{now_beirut.strftime("%A, %B %-d, %Y")} &nbsp;·&nbsp; Beirut</div>
  </div>

  <div class="body">

    <!-- VERSE -->
    <div class="section">
      <div class="label">📖 &nbsp;Verse of the Day</div>
      <div class="verse-text">"{verse["text"]}"</div>
      <div class="verse-ref">{verse["reference"]}</div>
    </div>

    <!-- WEATHER -->
    <div class="section section-white">
      <div class="label">🌤️ &nbsp;Weather · Beirut</div>
      {weather_today_html}
      {weather_compact_html}
    </div>

    <!-- NEWS -->
    <div class="section">
      <div class="label">🗞️ &nbsp;Top International News</div>
      <table width="100%" cellspacing="0" cellpadding="0">{news_html_items}</table>
    </div>

    <!-- FUN FACT -->
    <div class="section section-white">
      <div class="label">🧠 &nbsp;Fun Fact</div>
      <div class="fact-text">{fun_fact}</div>
    </div>

    <!-- QUOTE -->
    <div class="section section-dark">
      <div class="label label-light">💬 &nbsp;Quote of the Day</div>
      <div class="quote-text">"{quote["text"]}"</div>
      <div class="quote-author">— {quote["author"]}</div>
    </div>

    <!-- GUITAR -->
    <div class="section section-white">
      <div class="label">🎸 &nbsp;Guitar Pick</div>
      <div style="font-size:17px;font-weight:700;color:#1a1a2e;margin-bottom:2px;">{song["title"]}</div>
      <div style="font-size:13px;color:#666;margin-bottom:8px;">{song["artist"]}</div>
      <span class="badge" style="background:{song_dc};">{song["difficulty"].title()}</span>
      <span class="chords">{song["chords"]}</span>
    </div>

    <!-- ADVENTURE -->
    <div class="section">
      <div class="label">🏕️ &nbsp;Lebanon Adventure Pick</div>
      <div style="font-size:17px;font-weight:700;color:#1a1a2e;margin-bottom:3px;">{adventure["name"]}</div>
      <div style="margin-bottom:10px;">
        <span style="font-size:12px;color:#888;">{adventure["type"]}</span>
        &nbsp;·&nbsp;
        <span class="badge" style="background:{adv_dc};">{adventure["difficulty"].title()}</span>
      </div>
      <div style="font-size:14px;line-height:1.6;color:#444;">{adventure["description"]}</div>
    </div>

  </div>

  <div class="footer">Have a strong day! 🌞</div>

</div>
</div>
</body>
</html>"""

    return {"text": "\n".join(lines), "html": html}


if __name__ == "__main__":
    content = build_daily_message()
    logger.info("Daily content built successfully")
    print(content["text"])
    send_email(content)
    logger.info("Email sent successfully")
