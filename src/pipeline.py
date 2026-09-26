from collections import defaultdict
from datetime import date

from src.birthdays import get_upcoming_birthdays
from src.db import get_people
from src.notifier import send_notification


REMINDER_DAYS = 2
UPCOMING_COUNT = 4


def fetch_people() -> list[dict]:
    """Fetch people and their notification recipients."""
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
    """Return birthdays that need a reminder."""

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
    """Build a notification message."""

    lines = []

    if reminders:
        lines.append("🎂 Birthday reminder\n")

        for person in reminders:
            birthday = format_birthday_date(
                person["next_birthday"]
            )

            lines.append(
                f"• {person['name']} has a birthday in "
                f"{person['days_until']} days ({birthday})."
            )

        lines.append("")

    if upcoming:
        lines.append("📅 Next birthdays\n")

        for person in upcoming:
            birthday = format_birthday_date(
                person["next_birthday"]
            )

            lines.append(
                f"• {person['name']} — {birthday} "
                f"({person['days_until']} days)"
            )

    return "\n".join(lines)


def group_birthdays_by_recipient(
    birthdays: list[dict],
) -> dict[int, dict]:
    """
    Group birthdays by recipient.

    Each recipient gets only birthdays that they are
    associated with in person_recipients.
    """

    grouped: dict[int, dict] = {}

    for person in birthdays:
        for relationship in person.get(
            "person_recipients",
            [],
        ):
            recipient = relationship["recipients"]

            recipient_id = recipient["id"]

            if recipient_id not in grouped:
                grouped[recipient_id] = {
                    "recipient": recipient,
                    "birthdays": [],
                }

            grouped[recipient_id]["birthdays"].append(person)

    return grouped


def run_pipeline() -> None:
    """Run the birthday notification pipeline."""

    people = fetch_people()

    birthdays = calculate_upcoming_birthdays(people)

    reminders = get_reminder_birthdays(birthdays)

    if not reminders:
        return

    birthdays_by_recipient = group_birthdays_by_recipient(
        birthdays
    )

    for recipient_data in birthdays_by_recipient.values():
        recipient = recipient_data["recipient"]
        recipient_birthdays = recipient_data["birthdays"]

        recipient_reminders = [
            person
            for person in recipient_birthdays
            if person["days_until"] == REMINDER_DAYS
        ]

        if not recipient_reminders:
            continue

        recipient_upcoming = get_next_birthdays(
            recipient_birthdays
        )

        message = build_notification(
            reminders=recipient_reminders,
            upcoming=recipient_upcoming,
        )

        send_notification(
            message=message,
            recipient=recipient["email"],
        )