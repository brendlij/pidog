import logging


def setup_logging():
    logging.basicConfig(
        filename="logs.txt",
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        encoding="utf-8"
    )