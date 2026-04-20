import os
import smtplib
from pathlib import Path
from email.message import EmailMessage


def _load_env_file():
    env_path = Path(__file__).with_name(".env")
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def send_email(content):
    _load_env_file()
    sender_email = os.getenv("DAILY_FEED_EMAIL")
    sender_password = os.getenv("DAILY_FEED_PASSWORD")
    recipient_email = os.getenv("DAILY_FEED_RECIPIENT", sender_email)

    if not sender_email or not sender_password:
        raise ValueError("Set DAILY_FEED_EMAIL and DAILY_FEED_PASSWORD environment variables.")

    msg = EmailMessage()
    msg["Subject"] = "Your Daily Inspiration Feed"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(content["text"])
    msg.add_alternative(content["html"], subtype="html")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
