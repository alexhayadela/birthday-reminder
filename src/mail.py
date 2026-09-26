import smtplib
from email.mime.text import MIMEText

from src.config import Config


def send_mail(text: str, recipient: str) -> None:
    """Send a plain-text email to the recipient."""
    config = Config()

    sender = config.EMAIL_USER
    password = config.EMAIL_PASSWORD

    message = MIMEText(text, "plain")
    message["Subject"] = "🎂 Birthday reminders"
    message["From"] = sender
    message["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, message.as_string())