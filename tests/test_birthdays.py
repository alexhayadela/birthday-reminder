from datetime import date

from src.birthdays import (
    days_until_birthday,
    get_upcoming_birthdays,
    next_birthday,
)


def test_birthday_today() -> None:
    today = date(2026, 9, 26)

    assert days_until_birthday(
        9,
        26,
        today,
    ) == 0


def test_birthday_tomorrow() -> None:
    today = date(2026, 9, 26)

    assert days_until_birthday(
        9,
        27,
        today,
    ) == 1


def test_birthday_moves_to_next_year() -> None:
    today = date(2026, 9, 26)

    assert next_birthday(
        9,
        25,
        today,
    ) == date(2027, 9, 25)


def test_upcoming_birthdays_are_sorted() -> None:
    today = date(2026, 9, 26)

    people = [
        {
            "id": 1,
            "name": "Alice",
            "birthday_month": 12,
            "birthday_day": 1,
        },
        {
            "id": 2,
            "name": "Bob",
            "birthday_month": 9,
            "birthday_day": 28,
        },
    ]

    result = get_upcoming_birthdays(
        people,
        today,
    )

    assert result[0]["name"] == "Bob"
    assert result[1]["name"] == "Alice"