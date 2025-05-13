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


def load_config(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def extract_scraper_params(param_dict: dict) -> dict:
    try:
        param_keys = list(param_dict.keys())
        start_idx = param_keys.index("current_cities")
        end_idx = param_keys.index("hopping_freq") + 1
        param_dict = {key: param_dict[key] for key in param_keys[start_idx:end_idx]}
    except:
        raise ValueError("Can't parse ")

    return param_dict


def load_template_task(path: str) -> dict:
    with open(path, "r") as f:
        param_dict = json.load(f)
        return extract_scraper_params(param_dict)
