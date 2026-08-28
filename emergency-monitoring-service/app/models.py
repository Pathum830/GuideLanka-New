import uuid
from datetime import datetime

from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.database import Base


def _uuid() -> str:
    return str(uuid.uuid4())


class Vehicle(Base):
    """A safari vehicle in active operation.

    In the shared schema this table is likely owned/populated by the
    booking module (Member 2) -- this service mainly reads from it and
    appends pings/alerts.
    """
    __tablename__ = "vehicles"

    id = Column(String, primary_key=True, default=_uuid)
    driver_id = Column(String, nullable=True)
    trail_id = Column(String, ForeignKey("trail_points.trail_id"), nullable=True)
    is_active = Column(Boolean, default=True)

    pings = relationship("GPSPing", back_populates="vehicle")


class TrailPoint(Base):
    """A point along a mapped safari trail, used for deviation checks.

    Several rows share the same trail_id, ordered by `sequence`, forming
    a polyline. Real trail data would come from the park's GIS / mapping
    module -- seed a few points per trail for local testing.
    """
    __tablename__ = "trail_points"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trail_id = Column(String, index=True)
    sequence = Column(Integer)
    latitude = Column(Float)
    longitude = Column(Float)
    is_rest_area = Column(Boolean, default=False)


class GPSPing(Base):
    """A single GPS position update from a vehicle."""
    __tablename__ = "gps_pings"

    id = Column(String, primary_key=True, default=_uuid)
    vehicle_id = Column(String, ForeignKey("vehicles.id"), index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    vehicle = relationship("Vehicle", back_populates="pings")


class Alert(Base):
    """An emergency alert raised by the detection logic."""
    __tablename__ = "alerts"

    id = Column(String, primary_key=True, default=_uuid)
    vehicle_id = Column(String, ForeignKey("vehicles.id"), index=True)
    alert_type = Column(String)  # "stationary" | "deviation"
    detail = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime, nullable=True)
