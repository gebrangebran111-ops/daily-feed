import os
import smtplib
from email.message import EmailMessage


def send_email(content):
    sender_email = os.getenv("DAILY_FEED_EMAIL")
    sender_password = os.getenv("DAILY_FEED_PASSWORD")
    recipient_email = os.getenv("DAILY_FEED_RECIPIENT", sender_email)

    if not sender_email or not sender_password:
        raise ValueError("Set DAILY_FEED_EMAIL and DAILY_FEED_PASSWORD environment variables.")

    msg = EmailMessage()
    msg["Subject"] = "Your Daily Inspiration Feed"
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg.set_content(content)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)