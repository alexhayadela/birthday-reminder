import logging
import smtplib
from email.mime.text import MIMEText

from src.config import Config


logger = logging.getLogger(__name__)


def send_mail(text: str, recipient: str) -> None:
    """Send a plain-text email to the recipient."""

    logger.info("Preparing birthday email for recipient")

    config = Config()

    message = MIMEText(text, "plain")
    message["Subject"] = "🎂 Birthday reminders"
    message["From"] = config.EMAIL_USER
    message["To"] = recipient

    logger.debug(
        "Email prepared: subject=%s, message_length=%d",
        message["Subject"],
        len(text),
    )

    logger.info("Connecting to email server")

    with smtplib.SMTP_SSL(
        config.EMAIL_HOST,
        config.EMAIL_PORT,
    ) as server:
        server.login(
            config.EMAIL_USER,
            config.EMAIL_PASSWORD,
        )

        logger.debug("Email server authentication successful")

        server.sendmail(
            config.EMAIL_USER,
            recipient,
            message.as_string(),
        )

    logger.info("Birthday email sent successfully")