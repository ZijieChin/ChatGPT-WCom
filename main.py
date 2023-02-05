from conf import conf_reader

from loguru import logger

if __name__ == "__main__":
    logger.add(
        "./logs/run.log",
        encoding="utf-8",
        format="{level} | {time:YYYY-MM-DD HH:mm:ss} | {file} | {line} | {message}",
        retention="30 days",
        rotation="50 MB"
    )

    logger.info("System initializing...")
    conf = conf_reader()
