import logging
from app.config import config

logging.basicConfig(
    level=getattr(logging, config.LOGGING_LEVEL.upper(), logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s"
)

logger = logging.getLogger("app")