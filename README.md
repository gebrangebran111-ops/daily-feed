# Daily Feed

An automated Python project that sends a beautiful daily newsletter to your inbox every morning at 7 AM Beirut time, powered by GitHub Actions.

## What's Inside Every Email

| Section | Source |
|---|---|
| 📖 Verse of the Day | bolls.life API (random NIV verse) |
| 🌤️ Weather — 7 day forecast | Open-Meteo API (Beirut) |
| 🗞️ Top International News | GNews API (3 headlines with links) |
| 🧠 Fun Fact | Useless Facts API |
| 💬 Quote of the Day | Curated list, rotates daily |
| 🎸 Guitar Pick | Curated list, rotates daily |
| 🏕️ Lebanon Adventure Pick | Curated list, rotates daily |

## Project Structure

```
daily-feed/
├── main.py                          # Builds and sends the email
├── services/
│   ├── daily_content_service.py     # Fetches all content + curated picks
│   ├── email_service.py             # Gmail SMTP sender
│   └── openai_service.py            # (unused, kept for reference)
└── .github/
    └── workflows/
        └── daily.yml                # GitHub Actions cron schedule
```

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/GebranGebran/daily-feed.git
cd daily-feed
```

### 2. Get your API keys

| Key | Where to get it | Free tier |
|---|---|---|
| Gmail App Password | [myaccount.google.com](https://myaccount.google.com) → Security → App Passwords | Free |
| GNews API key | [gnews.io](https://gnews.io) → Sign up | 100 req/day |

> Use a Gmail **App Password**, not your regular Gmail password. 2-Step Verification must be enabled on your Google account first.

### 3. Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Value |
|---|---|
| `EMAIL_USER` | Your Gmail address (e.g. `you@gmail.com`) |
| `EMAIL_PASS` | Your Gmail App Password |
| `EMAIL_RECIPIENT` | Address to receive the email (can be same as `EMAIL_USER`) |
| `GNEWS_API_KEY` | Your GNews API key |

### 4. Enable the workflow

Go to **Actions** in your repo and make sure the `Daily Email` workflow is enabled. Then click **Run workflow** once manually to verify everything works.

## How the Schedule Works

The workflow runs automatically every day at **4 AM UTC (7 AM Beirut time)** via this cron:

```yaml
cron: "0 4 * * *"
```

A `.last_run` file is committed after each run to keep the repo active — GitHub disables scheduled workflows on inactive repos after 60 days of no commits.

> GitHub's scheduler is not always precise. Expect the email to arrive anywhere between 7–9 AM Beirut time depending on GitHub's server load.

## Curated Content

The **Quote of the Day**, **Guitar Pick**, and **Lebanon Adventure Pick** sections do not use any external API. They are picked from curated lists inside `daily_content_service.py` using today's date as a seed, so each day gets a different pick that is consistent for that day.

To add or change picks, edit the `_QUOTES`, `_SONGS`, and `_ADVENTURES` lists directly in `services/daily_content_service.py`.

## Customization

**Change the send time** — edit the cron in `.github/workflows/daily.yml`. Times are in UTC (Beirut is UTC+3).

**Change the recipient** — update the `EMAIL_RECIPIENT` secret in GitHub.

**Add more quotes/songs/adventures** — append entries to the relevant list in `daily_content_service.py` following the existing format.

**Change weather location** — edit `lat, lon` in `get_weather()` inside `daily_content_service.py`.

## Troubleshooting

**Email not arriving** — Check your spam folder and add your sender Gmail address to contacts.

**Scheduled run not firing** — Go to Actions, open the workflow, and click "Run workflow" manually once. This resets GitHub's scheduler. The `.last_run` commit after each run prevents the repo from going inactive.

**GNews returning no articles** — You may have hit the 100 req/day free tier limit. The email will still send with a fallback message in the news section.

**Secrets missing** — If any secret is missing, the run will fail with a clear error in the Actions log naming which variable is not set.
