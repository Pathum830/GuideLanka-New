"""Integration tests: exercise the real FastAPI route + a throwaway SQLite DB.

Alerts fall back to log-only in this environment since no Firebase
credentials are present -- see app/services/alerts.py -- so these tests
only assert on the HTTP response and DB state, not on FCM delivery.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Vehicle, TrailPoint

from fastapi.testclient import TestClient

TEST_DB_URL = "sqlite:///:memory:"
# StaticPool keeps a single shared connection alive for the whole test --
# without it, each session would get its own throwaway in-memory DB.
engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    # Seed a vehicle with a short mapped trail.
    db = TestingSessionLocal()
    db.add(Vehicle(id="veh-1", trail_id="trail-A", is_active=True))
    db.add_all([
        TrailPoint(trail_id="trail-A", sequence=0, latitude=6.3720, longitude=81.5180),
        TrailPoint(trail_id="trail-A", sequence=1, latitude=6.3730, longitude=81.5190),
    ])
    db.commit()
    db.close()

    with TestClient(app) as c:
        yield c

    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_ping_on_trail_is_ok(client):
    resp = client.post("/gps/ping", json={
        "vehicle_id": "veh-1",
        "latitude": 6.3720,
        "longitude": 81.5180,
    })
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_ping_far_from_trail_triggers_deviation_alert(client):
    resp = client.post("/gps/ping", json={
        "vehicle_id": "veh-1",
        "latitude": 6.3820,   # ~1.1km off the mapped trail
        "longitude": 81.5180,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "alert_triggered"
    assert body["alert_type"] == "deviation"

    alerts_resp = client.get("/alerts")
    assert alerts_resp.status_code == 200
    alerts = alerts_resp.json()
    assert len(alerts) == 1
    assert alerts[0]["alert_type"] == "deviation"
    assert alerts[0]["acknowledged"] is False


def test_ping_unknown_vehicle_returns_404(client):
    resp = client.post("/gps/ping", json={
        "vehicle_id": "does-not-exist",
        "latitude": 6.3720,
        "longitude": 81.5180,
    })
    assert resp.status_code == 404


def test_acknowledge_alert(client):
    client.post("/gps/ping", json={"vehicle_id": "veh-1", "latitude": 6.3820, "longitude": 81.5180})
    alert_id = client.get("/alerts").json()[0]["id"]

    resp = client.post(f"/alerts/{alert_id}/acknowledge")
    assert resp.status_code == 200
    assert resp.json()["acknowledged"] is True

    active = client.get("/alerts", params={"active_only": True}).json()
    assert active == []
