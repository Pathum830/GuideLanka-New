import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.jobs.sweep import start_scheduler, stop_scheduler
from app.routes import gps, alerts, health

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    start_scheduler()
    yield
    stop_scheduler()


app = FastAPI(
    title="GuideLanka — Emergency Monitoring & GPS Tracking",
    description="Member 4's module: FR9 (real-time vehicle monitoring) and FR10 (emergency detection & alerts).",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(gps.router)
app.include_router(alerts.router)
