import sys

import yaml
from loguru import logger


def conf_reader():
    try:
        with open("confg.yml", encoding="utf-8") as f:
            conf = yaml.safe_load(f)
    except Exception as e:
        logger.error(e)
        sys.exit("Exiting...")
    return conf
