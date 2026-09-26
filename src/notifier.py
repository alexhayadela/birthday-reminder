import logging

from src.mail import send_mail


logger = logging.getLogger(__name__)


def send_notification(message: str, recipient: str) -> None:
    """Send a notification."""

    logger.info("Sending notification")

    logger.debug(
        "Notification message length: %d characters",
        len(message),
    )

    # Today this is email.
    # Later this can be replaced by WhatsApp.
    send_mail(message, recipient)

    logger.info("Notification sent successfully")