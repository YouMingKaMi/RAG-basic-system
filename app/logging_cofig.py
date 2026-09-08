import logging
from pathlib import Path

def setup_logging():
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers = [
            logging.StreamHandler(),
            logging.FileHandler("logs/app.log",encoding="utf-8")
                    ]
    )