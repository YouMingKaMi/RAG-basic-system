import logging
from app.config import LOG_PATH
def setup_logging():
    LOG_PATH.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers = [
            logging.StreamHandler(),
            logging.FileHandler(LOG_PATH/"app.log",encoding="utf-8")
                    ]
    )