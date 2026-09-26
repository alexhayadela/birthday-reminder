import logging.config
from pathlib import Path

from src.pipeline import run_pipeline


LOGGING_CONFIG = (
    Path(__file__).resolve().parent
    / "conf"
    / "logging.conf"
)

logging.config.fileConfig(
    LOGGING_CONFIG,
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.info("Starting birthday application")

    run_pipeline()

    logger.info("Birthday application finished")