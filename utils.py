import os
import sys
import json
import logging


def setup_logger(debug: bool = False) -> None:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO if debug else logging.WARNING)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO if debug else logging.WARNING)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.handlers = []
    logger.addHandler(handler)


def load_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def init_dirs() -> None:
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("image", exist_ok=True)
