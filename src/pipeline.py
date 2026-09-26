from datetime import date

from src.birthdays import get_upcoming_birthdays
from src.db import get_people
from src.notifier import send_notification


REMINDER_DAYS = 2
UPCOMING_COUNT = 4


def fetch_people() -> list[dict]:
    """Fetch people from the database."""
    return get_people()


def calculate_upcoming_birthdays(
    people: list[dict],
) -> list[dict]:
    """Calculate and sort everyone's next birthday."""

    return get_upcoming_birthdays(people)


def get_reminder_birthdays(
    birthdays: list[dict],
    reminder_days: int = REMINDER_DAYS,
) -> list[dict]:
    """Return birthdays that need a reminder today."""

    return [
        person
        for person in birthdays
        if person["days_until"] == reminder_days
    ]


def get_next_birthdays(
    birthdays: list[dict],
    count: int = UPCOMING_COUNT,
) -> list[dict]:
    """Return the next N upcoming birthdays."""

    return birthdays[:count]


def format_birthday_date(birthday: date) -> str:
    """Format a birthday for display."""
    return birthday.strftime("%A, %d %B")


def build_notification(
    reminders: list[dict],
    upcoming: list[dict],
) -> str:
    """Build the notification message."""

    lines = []

    if reminders:
        lines.append("🎂 Birthday reminder\n")

        for person in reminders:
            birthday = format_birthday_date(person["next_birthday"])

            lines.append(
                f"• {person['name']} has a birthday in "
                f"2 days ({birthday})."
            )

        lines.append("")

    lines.append("📅 Next birthdays\n")

    for person in upcoming:
        birthday = format_birthday_date(person["next_birthday"])

        lines.append(
            f"• {person['name']} — {birthday} "
            f"({person['days_until']} days)"
        )

    return "\n".join(lines)


def should_notify(reminders: list[dict]) -> bool:
    """Return True when a birthday reminder should be sent."""
    return bool(reminders)


def run_pipeline() -> None:
    """Run the birthday notification pipeline."""

    people = fetch_people()

    birthdays = calculate_upcoming_birthdays(people)

    reminders = get_reminder_birthdays(birthdays)

    if not should_notify(reminders):
        return

    upcoming = get_next_birthdays(birthdays)

    message = build_notification(
        reminders=reminders,
        upcoming=upcoming,
    )

    # Recipient can later be changed independently of the pipeline.
    from src.config import Config

    config = Config()

    send_notification(
        message=message,
        recipient=config.EMAIL_USER,
    )