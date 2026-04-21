# Daily Feed

Daily Feed is an automated Python project that sends a daily newsletter-style email with:

- a Verse of the Day
- weather in Beirut (today + tomorrow)
- up to 3 major international headlines
- a Fun Fact of the Day
- a Quote of the Day from a real person
- an AI-generated guitar song pick
- an AI-generated location/adventure pick in Lebanon

Content is gathered from APIs and OpenAI, formatted into clean text + HTML, and delivered via Gmail SMTP.

## What This Project Does

On each run, the app:

1. Fetches verse, weather, news, fun fact, and real-person quote
2. Uses OpenAI to generate a guitar pick and Lebanon location pick
3. Builds a modern newsletter layout with clean card sections
4. Logs each section fetch and errors clearly (useful in GitHub Actions logs)
5. Sends the email to your configured recipient

## Project Structure

- `main.py` - main flow (generate content, build email, send)
- `services/daily_content_service.py` - fetch logic for verse/weather/news/fact/quote + AI section merge
- `services/openai_service.py` - OpenAI call for guitar + location recommendations with retry
- `services/email_service.py` - Gmail SMTP email sender
- `.github/workflows/daily.yml` - scheduled GitHub Action
- `services/.env` - local environment variables (not committed)

## Setup (Local)

### 1) Clone and open project

```bash
git clone <your-repo-url>
cd daily-feed
```

### 2) Create local env file

Create `services/.env`:

```env
DAILY_FEED_EMAIL="you@gmail.com"
DAILY_FEED_PASSWORD="your_gmail_app_password"
DAILY_FEED_RECIPIENT="you@gmail.com"
OPENAI_API_KEY="your_openai_api_key"
NEWSAPI_KEY="your_newsapi_key"
```

Notes:
- Use a Gmail **App Password** (not your normal Gmail password).
- Keep `.env` private (already ignored in `.gitignore`).

### 3) Run locally

```bash
python main.py
```

## How to Add GitHub Secrets

In your GitHub repo:

1. Go to `Settings` -> `Secrets and variables` -> `Actions`
2. Click `New repository secret`
3. Add these secrets:
   - `EMAIL_USER` -> your Gmail address
   - `EMAIL_PASS` -> your Gmail App Password
   - `OPENAI_API_KEY` -> your OpenAI API key
   - `NEWSAPI_KEY` -> your NewsAPI key

The workflow maps these secrets to runtime env vars used by your script.

## How to Run the GitHub Action

### Manual run

1. Open your repo on GitHub
2. Go to `Actions`
3. Select `Daily Email`
4. Click `Run workflow`

### Scheduled run

The workflow also runs automatically on the cron schedule in:

- `.github/workflows/daily.yml`

Current schedule:

```yaml
cron: "0 4 * * *"
```

This is UTC time. Adjust if you want a specific Lebanon local time.

## How to Customize Email Content

### Change AI guitar and location behavior

Edit prompt text in:

- `services/openai_service.py`

You can customize:
- guitar difficulty preference
- music genre and era variation
- location/adventure style in Lebanon

### Change email visual formatting

Edit email templates in:

- `main.py`

There are two formats:
- `text` version (plain email clients)
- `html` version (newsletter layout)

You can update:
- section titles
- emojis
- spacing
- colors and card style in HTML

## Automation Status

Once secrets are set and workflow is enabled, the system is fully automatic:

- GitHub Actions runs hourly and sends only at 7 AM Beirut time
- APIs + OpenAI generate the newsletter content
- email is sent automatically

