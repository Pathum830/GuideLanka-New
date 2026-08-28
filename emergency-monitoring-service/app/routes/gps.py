from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GPSPing, Vehicle
from app.schemas import GPSPingIn, PingResponse
from app.services.detection import check_deviation
from app.services.alerts import trigger_alert

router = APIRouter(prefix="/gps", tags=["gps"])


@router.post("/ping", response_model=PingResponse)
def receive_ping(ping: GPSPingIn, db: Session = Depends(get_db)):
    vehicle = db.query(Vehicle).filter(Vehicle.id == ping.vehicle_id).first()
    if vehicle is None:
        raise HTTPException(status_code=404, detail=f"Unknown vehicle_id '{ping.vehicle_id}'")

    record = GPSPing(
        vehicle_id=ping.vehicle_id,
        latitude=ping.latitude,
        longitude=ping.longitude,
        timestamp=ping.timestamp or datetime.utcnow(),
    )
    db.add(record)
    db.commit()

    # Deviation is cheap enough to check on every ping. Stationary
    # detection needs a time window and runs separately (see jobs/sweep.py).
    result = check_deviation(db, ping.vehicle_id, ping.latitude, ping.longitude)
    if result.triggered:
        trigger_alert(db, ping.vehicle_id, result.alert_type, result.detail)
        return PingResponse(status="alert_triggered", alert_type=result.alert_type, detail=result.detail)

    return PingResponse(status="ok")
