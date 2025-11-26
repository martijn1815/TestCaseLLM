import logging

from src.config.settings import settings


# Create and configure logger
logging.basicConfig(
    filename=settings.log_file,
    format="{asctime} - {levelname} - {name} - {message}",
    style="{",
    level=logging.INFO
)

logger = logging.getLogger()
