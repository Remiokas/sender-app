import contextlib

from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from app.config import CONFIG
from app.events.tasks import send_event
from app.utils import run_async_job


def create_scheduler() -> BackgroundScheduler:
    scheduler = BackgroundScheduler()
    trigger = IntervalTrigger(seconds=CONFIG.SEND_INTERVAL)
    scheduler.add_job(run_async_job, trigger, args=[send_event])
    return scheduler


@contextlib.asynccontextmanager
async def lifespan_handler(app):
    scheduler = create_scheduler()
    scheduler.start()

    yield

    scheduler.shutdown()


app = FastAPI(lifespan=lifespan_handler)


@app.get("/")
async def healthcheck():
    return {"message": "Hello World"}
