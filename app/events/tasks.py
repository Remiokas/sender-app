from app.events.methods import collect_event_data, send_request
from app.utils import logger


async def send_event():
    logger.info("Event sending started...")
    event = await collect_event_data()
    await send_request(event)
