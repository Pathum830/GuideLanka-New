"""Core detection logic for FR9 / FR10.

Kept free of FastAPI/DB-session concerns where possible so the rules
themselves (`nearest_distance_to_trail`, `is_cluster_stationary`) can be
unit tested as plain functions -- see tests/test_detection.py.
"""
from datetime import datetime, timedelta
from typing import Iterable, Optional

from geopy.distance import geodesic
from sqlalchemy.orm import Session

from app.config import settings
from app.models import GPSPing, TrailPoint, Vehicle
from app.schemas import DetectionResult


# ---------------------------------------------------------------------
# Pure geometry helpers (no DB access -- easy to unit test)
# ---------------------------------------------------------------------

def nearest_distance_to_trail(
    position: tuple[float, float],
    trail_points: Iterable[tuple[float, float]],
) -> float:
    """Distance in meters from `position` to the closest point in `trail_points`.

    This is a nearest-vertex approximation, not point-to-segment distance --
    good enough when trail points are sampled densely (e.g. every ~20-50m).
    If trail points are sparse, consider projecting onto each segment instead.
    """
    trail_points = list(trail_points)
    if not trail_points:
        # No mapped trail for this vehicle -- can't evaluate deviation.
        return 0.0
    return min(geodesic(position, tp).meters for tp in trail_points)


def is_cluster_stationary(
    positions: Iterable[tuple[float, float]],
    radius_m: float,
) -> bool:
    """True if every position falls within `radius_m` of the first one.

    Uses a fixed reference point (the earliest ping) rather than a
    centroid, which is enough to absorb normal GPS jitter while still
    catching genuine drift.
    """
    positions = list(positions)
    if len(positions) < 2:
        return False
    anchor = positions[0]
    return all(geodesic(anchor, p).meters <= radius_m for p in positions)


# ---------------------------------------------------------------------
# DB-aware checks used by the API routes / scheduled job
# ---------------------------------------------------------------------

def check_deviation(db: Session, vehicle_id: str, lat: float, lon: float) -> DetectionResult:
    """Per-ping check: has the vehicle strayed from its mapped trail?"""
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()
    if vehicle is None or not vehicle.trail_id:
        return DetectionResult(triggered=False)

    trail_rows = (
        db.query(TrailPoint)
        .filter(TrailPoint.trail_id == vehicle.trail_id)
        .order_by(TrailPoint.sequence)
        .all()
    )
    trail_points = [(tp.latitude, tp.longitude) for tp in trail_rows]

    distance_m = nearest_distance_to_trail((lat, lon), trail_points)

    if distance_m > settings.DEVIATION_THRESHOLD_METERS:
        return DetectionResult(
            triggered=True,
            alert_type="deviation",
            detail=f"{distance_m:.0f}m from mapped trail (threshold {settings.DEVIATION_THRESHOLD_METERS:.0f}m)",
        )
    return DetectionResult(triggered=False)


def _vehicle_in_rest_area(db: Session, vehicle: Vehicle, lat: float, lon: float) -> bool:
    if not vehicle.trail_id:
        return False
    rest_points = (
        db.query(TrailPoint)
        .filter(TrailPoint.trail_id == vehicle.trail_id, TrailPoint.is_rest_area.is_(True))
        .all()
    )
    return any(
        geodesic((lat, lon), (rp.latitude, rp.longitude)).meters <= settings.STATIONARY_RADIUS_METERS
        for rp in rest_points
    )


def check_stationary(db: Session, vehicle: Vehicle) -> DetectionResult:
    """Window check: has this vehicle been still for too long outside a rest area?

    Intended to be called once per vehicle from the periodic sweep job,
    not per-ping, since it needs a time window of history to evaluate.
    """
    cutoff = datetime.utcnow() - timedelta(minutes=settings.STATIONARY_THRESHOLD_MINUTES)
    recent = (
        db.query(GPSPing)
        .filter(GPSPing.vehicle_id == vehicle.id, GPSPing.timestamp >= cutoff)
        .order_by(GPSPing.timestamp)
        .all()
    )

    if len(recent) < 2:
        # Not enough history yet in this window to make a call.
        return DetectionResult(triggered=False)

    latest = recent[-1]
    if _vehicle_in_rest_area(db, vehicle, latest.latitude, latest.longitude):
        return DetectionResult(triggered=False)

    positions = [(p.latitude, p.longitude) for p in recent]
    if is_cluster_stationary(positions, settings.STATIONARY_RADIUS_METERS):
        return DetectionResult(
            triggered=True,
            alert_type="stationary",
            detail=f"No movement for over {settings.STATIONARY_THRESHOLD_MINUTES} min",
        )
    return DetectionResult(triggered=False)
