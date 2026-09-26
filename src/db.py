import logging

from supabase import Client, create_client

from src.config import Config


logger = logging.getLogger(__name__)

config = Config()

supabase: Client = create_client(
    config.SUPABASE_URL,
    config.SUPABASE_API_KEY,
)

logger.info("Supabase client initialized")


def get_people() -> list[dict]:
    """Return all people with their notification recipients."""

    logger.info("Fetching people and notification relationships")

    logger.debug(
        "Supabase query: table=people, "
        "select=id,name,birthday_month,birthday_day,"
        "person_recipients(recipient_id,recipients(id,name,email))"
    )

    response = (
        supabase
        .table("people")
        .select(
            """
            id,
            name,
            birthday_month,
            birthday_day,
            person_recipients(
                recipient_id,
                recipients(
                    id,
                    name,
                    email
                )
            )
            """
        )
        .execute()
    )

    records = response.data

    logger.info(
        "Fetched %d people from Supabase",
        len(records),
    )

    logger.debug(
        "People returned: %s",
        [
            {
                "id": person["id"],
                "name": person["name"],
                "birthday_month": person["birthday_month"],
                "birthday_day": person["birthday_day"],
            }
            for person in records
        ],
    )

    return records


def get_recipients() -> list[dict]:
    """Return all notification recipients."""

    logger.info("Fetching notification recipients")

    logger.debug(
        "Supabase query: table=recipients, select=id,name,email"
    )

    response = (
        supabase
        .table("recipients")
        .select("id, name, email")
        .execute()
    )

    records = response.data

    logger.info(
        "Fetched %d recipients from Supabase",
        len(records),
    )

    logger.debug(
        "Recipients returned: %s",
        [
            {
                "id": recipient["id"],
                "name": recipient["name"],
                "email": recipient["email"],
            }
            for recipient in records
        ],
    )

    return records