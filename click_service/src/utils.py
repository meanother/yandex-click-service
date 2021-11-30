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

ua_list = [  # needs to have more options
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
]


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
