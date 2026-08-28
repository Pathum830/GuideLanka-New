from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class GPSPingIn(BaseModel):
    """Payload the driver app (Member 2) posts to /gps/ping."""
    vehicle_id: str
    latitude: float
    longitude: float
    timestamp: Optional[datetime] = None


class PingResponse(BaseModel):
    status: str
    alert_type: Optional[str] = None
    detail: Optional[str] = None


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    vehicle_id: str
    alert_type: str
    detail: str
    created_at: datetime
    acknowledged: bool
    acknowledged_at: Optional[datetime] = None


class DetectionResult(BaseModel):
    triggered: bool
    alert_type: Optional[str] = None
    detail: Optional[str] = None
