import json
from random import choice
from typing import List, Dict

import requests

from app.config import CONFIG
from app.utils import logger


async def collect_event_data() -> List[Dict]:
    with open(f"{CONFIG.EVENT_JSON_PATH}", "r") as f:
        file_content = json.loads(f.read())
        random_event = [choice(file_content)]
    logger.info(f"Collected event {random_event}")
    return random_event


async def send_request(payload: List[Dict]):
    url = f"{CONFIG.EVENT_CONSUMER_URL}:{CONFIG.EVENT_CONSUMER_PORT}/event"
    try:
        r = requests.post(url, json=payload)
        if r.status_code == 200:
            logger.info(f"Event received successfully. {r.json()}")
        else:
            logger.info(f"Event sending failed. Error: {r.status_code} {r.json()}")
    except requests.exceptions.ConnectionError as ex:
        logger.error(ex)
