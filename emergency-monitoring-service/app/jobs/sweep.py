"""Periodic job that checks every active vehicle for the stationary trigger.

Runs on a timer (SWEEP_INTERVAL_MINUTES) rather than per-ping, since the
stationary check needs a window of ping history to evaluate, not just the
latest position.
"""
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.config import settings
from app.database import SessionLocal
from app.models import Vehicle
from app.services.detection import check_stationary
from app.services.alerts import trigger_alert

logger = logging.getLogger("emergency_monitoring.sweep")

_scheduler: BackgroundScheduler | None = None


def sweep_stationary_vehicles():
    db = SessionLocal()
    try:
        active_vehicles = db.query(Vehicle).filter(Vehicle.is_active.is_(True)).all()
        for vehicle in active_vehicles:
            result = check_stationary(db, vehicle)
            if result.triggered:
                trigger_alert(db, vehicle.id, result.alert_type, result.detail)
    except Exception:  # noqa: BLE001 -- one bad sweep shouldn't kill the scheduler
        logger.exception("Stationary sweep failed")
    finally:
        db.close()


def start_scheduler() -> BackgroundScheduler:
    global _scheduler
    if _scheduler is not None:
        return _scheduler

    _scheduler = BackgroundScheduler()
    _scheduler.add_job(
        sweep_stationary_vehicles,
        "interval",
        minutes=settings.SWEEP_INTERVAL_MINUTES,
        id="stationary_sweep",
    )
    _scheduler.start()
    logger.info("Stationary sweep scheduler started (every %s min)", settings.SWEEP_INTERVAL_MINUTES)
    return _scheduler


def stop_scheduler():
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None
