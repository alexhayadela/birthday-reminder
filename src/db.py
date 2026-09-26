from supabase import create_client, Client

from src.config import Config


config = Config()

supabase: Client = create_client(
    config.SUPABASE_URL,
    config.SUPABASE_API_KEY,
)
"""Returns a supabase client."""


def get_people() -> list[dict]:
    """Return all people with birthdays."""
    return (
        supabase
        .table("people")
        .select("id, name, birthday_month, birthday_day")
        .execute()
        .data
    )