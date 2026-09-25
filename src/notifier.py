from src.mail import send_mail


def send_notification(message: str, recipient: str) -> None:
    """Send a notification."""

    # Today this is email.
    # Later this can be replaced by WhatsApp.
    send_mail(message, recipient)