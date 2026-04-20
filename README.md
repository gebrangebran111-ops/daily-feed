# Daily Feed Newsletter

A simple Python project that sends one daily email with:

- an inspirational quote
- a guitar song with chords
- an outdoor adventure recommendation in Lebanon

The result is formatted like a clean mini newsletter so it feels enjoyable to read, not like raw logs.

## How It Works

Each run:

1. Loads previously used items from `used_items.json`
2. Picks a new quote, song, and location
3. Avoids repeating items until all choices in a category are used
4. Rotates difficulty:
   - songs: easy -> medium -> hard
   - adventures: easy -> medium -> hard
5. Avoids similar back-to-back picks:
   - avoids same song artist as yesterday when possible
   - avoids same adventure type as yesterday when possible
6. Sends a styled email (plain text + HTML)
7. Updates `used_items.json`

When all options in a category are consumed, that category is reset automatically and rotation continues.

## Project Structure

- `main.py` - orchestration, selection, formatting, send
- `data/quotes.py` - quote dataset and quote picker
- `data/songs.py` - song dataset with difficulty and song picker
- `data/locations.py` - Lebanon adventure dataset with difficulty and picker
- `services/email_service.py` - Gmail SMTP sender
- `services/used_items_service.py` - read/write/reset used items
- `used_items.json` - persisted history for rotation and anti-repeat logic
- `.github/workflows/daily.yml` - automation workflow

## Technologies Used

- Python 3.11
- Standard library only for app logic:
  - `smtplib`
  - `email.message`
  - `json`
  - `pathlib`
- GitHub Actions for daily scheduling
- Gmail SMTP (`smtp.gmail.com:587`)

## Local Run

Create `services/.env` (local only, never commit secrets):

```env
DAILY_FEED_EMAIL="you@gmail.com"
DAILY_FEED_PASSWORD="your_gmail_app_password"
DAILY_FEED_RECIPIENT="you@gmail.com"
```

Then run:

```bash
python main.py
```

## GitHub Actions Automation

Workflow file: `.github/workflows/daily.yml`

It runs daily using cron and can also be triggered manually.

Required repository secrets:

- `EMAIL_USER` - sender Gmail address
- `EMAIL_PASS` - Gmail App Password

The workflow maps these secrets to runtime env vars:

- `DAILY_FEED_EMAIL`
- `DAILY_FEED_PASSWORD`
- `DAILY_FEED_RECIPIENT`

To persist history between runs, the workflow commits updated `used_items.json` back to the repo.

## Is It Fully Automatic?

Yes. Once pushed and enabled:

- GitHub Actions runs at the scheduled UTC time every day
- It sends the newsletter email automatically
- It updates item history automatically

If a run fails, check the Actions logs. Common causes are expired Gmail app password or missing secrets.

