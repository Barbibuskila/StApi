from json import load as _load
from sys import exit as _exit
from loguru import logger


def read_config(path):
    """
    Reads configuration from json file
    :param path: path of the json file
    :return: python dict of the json configuration
    """
    try:
        with open(path, "r") as config_file:
            return _load(config_file)
    except Exception as err:
        logger.critical(f"Cannot read configuration - {err}")
        _exit(1)
