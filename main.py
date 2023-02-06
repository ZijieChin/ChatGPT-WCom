from apis import launch

from loguru import logger


logger.add(
    "./logs/run.log",
    encoding="utf-8",
    format="{level} | {time:YYYY-MM-DD HH:mm:ss} | {file} | {line} | {message}",
    retention="30 days",
    rotation="50 MB"
)


if __name__ == "__main__":
    logger.info("System initializing...")
    launch()
