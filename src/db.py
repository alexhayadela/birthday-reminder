from supabase import Client, create_client

from src.config import Config


config = Config()

supabase: Client = create_client(
    config.SUPABASE_URL,
    config.SUPABASE_API_KEY,
)
"""Returns a supabase client."""


def get_people() -> list[dict]:
    """Return all people with their notification recipients."""

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

    return response.data


def get_recipients() -> list[dict]:
    """Return all notification recipients."""

    response = (
        supabase
        .table("recipients")
        .select("id, name, email")
        .execute()
    )

    return response.data