from datetime import date, timedelta


def birthday_this_year(month: int, day: int, year: int) -> date:
    """Return a birthday as a date in the given year."""
    return date(year, month, day)


def days_until_birthday(
    month: int,
    day: int,
    today: date | None = None,
) -> int:
    """Return the number of days until the next occurrence of a birthday."""

    if today is None:
        today = date.today()

    try:
        birthday = birthday_this_year(month, day, today.year)
    except ValueError:
        # Handles Feb 29 in a non-leap year.
        birthday = date(today.year + 1, month, day)

    if birthday < today:
        birthday = birthday_this_year(month, day, today.year + 1)

    return (birthday - today).days


def next_birthday(
    month: int,
    day: int,
    today: date | None = None,
) -> date:
    """Return the date of the person's next birthday."""

    if today is None:
        today = date.today()

    days = days_until_birthday(month, day, today)

    return today + timedelta(days=days)


def get_upcoming_birthdays(
    people: list[dict],
    today: date | None = None,
) -> list[dict]:
    """Return people sorted by their next upcoming birthday."""

    if today is None:
        today = date.today()

    birthdays = []

    for person in people:
        birthday = next_birthday(
            person["birthday_month"],
            person["birthday_day"],
            today,
        )

        birthdays.append(
            {
                **person,
                "next_birthday": birthday,
                "days_until": (birthday - today).days,
            }
        )

    return sorted(
        birthdays,
        key=lambda person: person["next_birthday"],
    )