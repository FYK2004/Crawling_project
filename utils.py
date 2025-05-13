import sys
import json
import logging


def setup_logger(debug: bool = False) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG if debug else logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(handler)


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)

