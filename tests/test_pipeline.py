from datetime import date

from src.pipeline import (
    build_notification,
    group_birthdays_by_recipient,
)


def test_group_birthdays_by_recipient() -> None:
    birthdays = [
        {
            "id": 1,
            "name": "Alice",
            "next_birthday": date(2026, 9, 28),
            "days_until": 2,
            "person_recipients": [
                {
                    "recipient_id": 1,
                    "recipients": {
                        "id": 1,
                        "name": "Me",
                        "email": "me@example.com",
                    },
                },
                {
                    "recipient_id": 2,
                    "recipients": {
                        "id": 2,
                        "name": "Sister",
                        "email": "sister@example.com",
                    },
                },
            ],
        },
        {
            "id": 2,
            "name": "Bob",
            "next_birthday": date(2026, 9, 29),
            "days_until": 3,
            "person_recipients": [
                {
                    "recipient_id": 1,
                    "recipients": {
                        "id": 1,
                        "name": "Me",
                        "email": "me@example.com",
                    },
                },
            ],
        },
    ]

    result = group_birthdays_by_recipient(birthdays)

    assert len(result) == 2

    me_birthdays = result[1]["birthdays"]
    sister_birthdays = result[2]["birthdays"]

    assert [person["name"] for person in me_birthdays] == [
        "Alice",
        "Bob",
    ]

    assert [person["name"] for person in sister_birthdays] == [
        "Alice",
    ]


def test_notification_contains_only_recipient_birthdays() -> None:
    birthdays = [
        {
            "id": 1,
            "name": "Alice",
            "next_birthday": date(2026, 9, 28),
            "days_until": 2,
        },
    ]

    message = build_notification(
        reminders=birthdays,
        upcoming=birthdays,
    )

    assert "Alice" in message