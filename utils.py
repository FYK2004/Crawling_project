import os
import sys
import time
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
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def init_dirs() -> None:
    os.makedirs("tmp", exist_ok=True)
    os.makedirs("image", exist_ok=True)


def format_elapsed_time(start_time: float):
    end_time = time.time()
    elapsed_seconds = int(end_time - start_time)
    minutes = elapsed_seconds // 60
    seconds = elapsed_seconds % 60
    return f"{minutes:>2}m {seconds:02d}s"
