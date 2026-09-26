import logging
from datetime import date, timedelta


logger = logging.getLogger(__name__)


def birthday_this_year(month: int, day: int, year: int) -> date:
    """Return a birthday as a date in the given year."""

    birthday = date(year, month, day)

    logger.debug(
        "Created birthday date: month=%s, day=%s, year=%s -> %s",
        month,
        day,
        year,
        birthday,
    )

    return birthday


def days_until_birthday(
    month: int,
    day: int,
    today: date | None = None,
) -> int:
    """Return the number of days until the next occurrence of a birthday."""

    if today is None:
        today = date.today()

    logger.debug(
        "Calculating days until birthday: month=%s, day=%s, today=%s",
        month,
        day,
        today,
    )

    try:
        birthday = birthday_this_year(
            month,
            day,
            today.year,
        )
    except ValueError:
        logger.debug(
            "Birthday %s-%s does not exist in %s; treating it as next year's birthday",
            month,
            day,
            today.year,
        )

        birthday = date(
            today.year + 1,
            month,
            day,
        )

    if birthday < today:
        logger.debug(
            "Birthday %s has already passed; using next year",
            birthday,
        )

        birthday = birthday_this_year(
            month,
            day,
            today.year + 1,
        )

    days = (birthday - today).days

    logger.debug(
        "Next birthday=%s, days_until=%s",
        birthday,
        days,
    )

    return days


def next_birthday(
    month: int,
    day: int,
    today: date | None = None,
) -> date:
    """Return the date of the person's next birthday."""

    if today is None:
        today = date.today()

    days = days_until_birthday(
        month,
        day,
        today,
    )

    birthday = today + timedelta(days=days)

    logger.debug(
        "Calculated next birthday: %s-%s -> %s",
        month,
        day,
        birthday,
    )

    return birthday


def get_upcoming_birthdays(
    people: list[dict],
    today: date | None = None,
) -> list[dict]:
    """Return people sorted by their next upcoming birthday."""

    if today is None:
        today = date.today()

    logger.info(
        "Calculating upcoming birthdays for %d people",
        len(people),
    )

    birthdays = []

    for person in people:
        birthday = next_birthday(
            person["birthday_month"],
            person["birthday_day"],
            today,
        )

        logger.debug(
            "Birthday calculated: person=%s, next_birthday=%s, days_until=%s",
            person["name"],
            birthday,
            (birthday - today).days,
        )

        birthdays.append(
            {
                **person,
                "next_birthday": birthday,
                "days_until": (birthday - today).days,
            }
        )

    birthdays = sorted(
        birthdays,
        key=lambda person: person["next_birthday"],
    )

    logger.info(
        "Birthday calculation completed; %d birthdays sorted",
        len(birthdays),
    )

    return birthdays