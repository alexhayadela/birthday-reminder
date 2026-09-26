import logging
import os
from pathlib import Path

from dotenv import load_dotenv


logger = logging.getLogger(__name__)

ENV_PATH = Path(__file__).resolve().parents[1] / "conf" / ".env"


def load_env() -> None:
    """Load environment variables from the local .env file."""

    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)
        logger.info("Loaded environment from %s", ENV_PATH)
    else:
        logger.warning("Environment file not found: %s", ENV_PATH)


class Config:
    """Application configuration."""

    def __init__(self) -> None:
        logger.debug("Loading application configuration")

        load_env()

        self.SUPABASE_URL: str = self._required("SUPABASE_URL")
        self.SUPABASE_API_KEY: str = self._required("SUPABASE_API_KEY")

        self.EMAIL_HOST: str = self._required("EMAIL_HOST")
        self.EMAIL_PORT: int = int(self._required("EMAIL_PORT"))
        self.EMAIL_USER: str = self._required("EMAIL_USER")
        self.EMAIL_PASSWORD: str = self._required("EMAIL_PASSWORD")

        logger.info("Application configuration loaded")

    @staticmethod
    def _required(name: str) -> str:
        value = os.environ.get(name)

        if not value:
            logger.error(
                "Required environment variable is missing: %s",
                name,
            )
            raise ValueError(
                f"Missing required environment variable: {name}"
            )

        logger.debug("Configuration value loaded: %s", name)

        return value