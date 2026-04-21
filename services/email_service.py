import logging
import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr

logger = logging.getLogger("daily_feed.email")


def send_email(content):
    sender_email = os.getenv("DAILY_FEED_EMAIL")
    sender_password = os.getenv("DAILY_FEED_PASSWORD")
    recipient_email = os.getenv("DAILY_FEED_RECIPIENT", sender_email)

    if not sender_email:
        logger.error("DAILY_FEED_EMAIL env variable is missing")
        raise ValueError("DAILY_FEED_EMAIL environment variable is not set.")
    if not sender_password:
        logger.error("DAILY_FEED_PASSWORD env variable is missing")
        raise ValueError("DAILY_FEED_PASSWORD environment variable is not set.")

    logger.info("Sending email from %s to %s", sender_email, recipient_email)

    msg = EmailMessage()
    msg["Subject"] = "Your Daily Inspiration Feed"
    msg["From"] = formataddr(("Daily Feed", sender_email))
    msg["To"] = recipient_email
    msg.set_content(content["text"])
    msg.add_alternative(content["html"], subtype="html")

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

    logger.info("Email sent successfully to %s", recipient_email)
