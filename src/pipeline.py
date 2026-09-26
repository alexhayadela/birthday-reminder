import logging
from datetime import date

from src.birthdays import get_upcoming_birthdays
from src.db import get_people
from src.notifier import send_notification


logger = logging.getLogger(__name__)

REMINDER_DAYS = 2
UPCOMING_COUNT = 4


def fetch_people() -> list[dict]:
    """Fetch people and their notification recipients."""

    logger.info("Fetching people")

    people = get_people()

    logger.info(
        "Fetched %d people",
        len(people),
    )

    return people


def calculate_upcoming_birthdays(
    people: list[dict],
) -> list[dict]:
    """Calculate and sort everyone's next birthday."""

    logger.info(
        "Calculating upcoming birthdays for %d people",
        len(people),
    )

    birthdays = get_upcoming_birthdays(people)

    logger.debug(
        "Upcoming birthdays: %s",
        [
            {
                "name": person["name"],
                "next_birthday": person["next_birthday"],
                "days_until": person["days_until"],
            }
            for person in birthdays
        ],
    )

    return birthdays


def get_reminder_birthdays(
    birthdays: list[dict],
    reminder_days: int = REMINDER_DAYS,
) -> list[dict]:
    """Return birthdays that need a reminder."""

    reminders = [
        person
        for person in birthdays
        if person["days_until"] == reminder_days
    ]

    logger.info(
        "Found %d birthdays requiring a reminder in %d days",
        len(reminders),
        reminder_days,
    )

    logger.debug(
        "Reminder birthdays: %s",
        [person["name"] for person in reminders],
    )

    return reminders


def get_next_birthdays(
    birthdays: list[dict],
    count: int = UPCOMING_COUNT,
) -> list[dict]:
    """Return the next N upcoming birthdays."""

    upcoming = birthdays[:count]

    logger.debug(
        "Selected next %d birthdays: %s",
        count,
        [
            {
                "name": person["name"],
                "days_until": person["days_until"],
            }
            for person in upcoming
        ],
    )

    return upcoming


def format_birthday_date(birthday: date) -> str:
    """Format a birthday for display."""

    return birthday.strftime("%A, %d %B")


def build_notification(
    reminders: list[dict],
    upcoming: list[dict],
) -> str:
    """Build a notification message."""

    logger.debug(
        "Building notification: reminders=%d, upcoming=%d",
        len(reminders),
        len(upcoming),
    )

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

    if upcoming:
        lines.append("")
        lines.append("📅 Next birthdays\n")

        for person in upcoming:
            birthday = format_birthday_date(
                person["next_birthday"]
            )

            lines.append(
                f"• {person['name']} — {birthday} "
                f"({person['days_until']} days)"
            )

    message = "\n".join(lines)

    logger.debug(
        "Notification built: %d characters",
        len(message),
    )

    return message


def group_birthdays_by_recipient(
    birthdays: list[dict],
) -> dict[int, dict]:
    """
    Group birthdays by recipient.

    Each recipient gets only birthdays that they are
    associated with in person_recipients.
    """

    logger.info(
        "Grouping %d birthdays by recipient",
        len(birthdays),
    )

    grouped: dict[int, dict] = {}

    for person in birthdays:
        relationships = person.get(
            "person_recipients",
            [],
        )

        logger.debug(
            "Person %s has %d recipient relationships",
            person["name"],
            len(relationships),
        )

        for relationship in relationships:
            recipient = relationship["recipients"]
            recipient_id = recipient["id"]

            if recipient_id not in grouped:
                grouped[recipient_id] = {
                    "recipient": recipient,
                    "birthdays": [],
                }

            grouped[recipient_id]["birthdays"].append(person)

    logger.info(
        "Created birthday groups for %d recipients",
        len(grouped),
    )

    logger.debug(
        "Recipient birthday counts: %s",
        {
            recipient_id: len(data["birthdays"])
            for recipient_id, data in grouped.items()
        },
    )

    return grouped


def run_pipeline() -> None:
    """Run the birthday notification pipeline."""

    logger.info("========== Birthday pipeline started ==========")

    people = fetch_people()

    birthdays = calculate_upcoming_birthdays(people)

    reminders = get_reminder_birthdays(birthdays)

    if not reminders:
        logger.info(
            "No birthdays require a reminder today; pipeline finished"
        )
        return

    logger.info(
        "Processing %d reminder birthdays",
        len(reminders),
    )

    birthdays_by_recipient = group_birthdays_by_recipient(
        birthdays
    )

    for recipient_data in birthdays_by_recipient.values():
        recipient = recipient_data["recipient"]
        recipient_birthdays = recipient_data["birthdays"]

        logger.debug(
            "Processing recipient id=%s, birthdays=%d",
            recipient["id"],
            len(recipient_birthdays),
        )

        recipient_reminders = [
            person
            for person in recipient_birthdays
            if person["days_until"] == REMINDER_DAYS
        ]

        if not recipient_reminders:
            logger.debug(
                "Recipient id=%s has no birthdays requiring a reminder",
                recipient["id"],
            )
            continue

        logger.info(
            "Recipient id=%s has %d reminder birthdays",
            recipient["id"],
            len(recipient_reminders),
        )

        recipient_upcoming = get_next_birthdays(
            recipient_birthdays
        )

        message = build_notification(
            reminders=recipient_reminders,
            upcoming=recipient_upcoming,
        )

        logger.info(
            "Sending notification to recipient id=%s",
            recipient["id"],
        )

        send_notification(
            message=message,
            recipient=recipient["email"],
        )

    logger.info("========== Birthday pipeline finished ==========")