import argparse
import os
import pathlib
import time
from datetime import datetime, timezone
from functools import wraps

from fake_useragent import UserAgent
from loguru import logger

log_dir = pathlib.Path.home().joinpath("logs")
log_dir.mkdir(parents=True, exist_ok=True)
pwd = os.path.dirname(os.path.abspath(__file__))
ua = UserAgent()

logger.add(
    log_dir.joinpath("yandex-click-bot-service.log"),
    format="{time} [{level}] {module} {name} {function} - {message}",
    level="INFO",
    compression="zip",
    rotation="30 MB",
)


def get_work_time(func):
    @wraps(func)
    def timer(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        result_time = time.time() - start
        logger.info(
            f"Function: {func.__name__} worked are {str(round(result_time, 2))} seconds"
        )
        return result

    return timer


def get_datetime():
    return datetime.now(timezone.utc)
