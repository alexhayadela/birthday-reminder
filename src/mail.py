import smtplib
from email.mime.text import MIMEText

from src.config import Config


def send_mail(text: str, recipient: str) -> None:
    """Send a plain-text email to the recipient."""
    config = Config()

    message = MIMEText(text, "plain")
    message["Subject"] = "🎂 Birthday reminders"
    message["From"] = config.EMAIL_USER
    message["To"] = recipient

    with smtplib.SMTP_SSL(config.EMAIL_HOST, config.EMAIL_PORT) as server:
        server.starttls()
        server.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        server.sendmail(config.EMAIL_USER, recipient, message.as_string())