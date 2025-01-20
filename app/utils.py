import datetime
import logging
import asyncio
import os

from app.config import CONFIG


def create_log_file():
    cwd = os.getcwd()
    log_path = f"{cwd}/logs"
    os.makedirs(log_path, exist_ok=True)
    return f"{log_path}/{datetime.date.today()}.log"


logging.basicConfig(
    filename=create_log_file(),
    format="%(asctime)s %(message)s",
    filemode="a",
    level=CONFIG.LOG_LEVEL,
)

logger = logging.getLogger(__name__)


def run_async_job(coroutine):
    asyncio.run(coroutine())
