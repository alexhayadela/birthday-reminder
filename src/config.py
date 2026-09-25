import os
from pathlib import Path

from dotenv import load_dotenv


ENV_PATH = Path(__file__).resolve().parents[1] / "conf" / ".env"


def load_env() -> None:
    """Load environment variables from the local .env file."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)


class Config:
    """Application configuration."""

    def __init__(self) -> None:
        load_env()

        self.SUPABASE_URL = self._required("SUPABASE_URL")
        self.SUPABASE_API_KEY = self._required("SUPABASE_API_KEY")
        self.EMAIL_USER = self._required("EMAIL_USER")
        self.EMAIL_PASSWORD = self._required("EMAIL_PASSWORD")

    @staticmethod
    def _required(name: str) -> str:
        value = os.environ.get(name)

        if not value:
            raise ValueError(f"Missing required environment variable: {name}")

        return value