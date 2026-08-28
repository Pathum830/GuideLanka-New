# Emergency Monitoring & GPS Tracking — Member 4

GuideLanka's real-time vehicle monitoring and emergency alert module
(FR9, FR10), built as a standalone Python/FastAPI microservice.

## Quick start

```bash
python3 -m venv venv
. venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env           # edit if you have real Postgres/Firebase creds

uvicorn app.main:app --reload --port 8000
```

Without a `.env`, the service falls back to a local SQLite file
(`dev.db`) and logs alerts instead of pushing them via FCM — so you can
run and test everything before Postgres/Firebase are wired up.

Open http://127.0.0.1:8000/docs for interactive API docs (Swagger UI).

## Run the tests

```bash
python -m pytest -v
```

11 tests: 6 pure unit tests on the detection math (no DB), 5 integration
tests that exercise the real API routes against a throwaway SQLite DB.

## Seeding a vehicle for manual testing

The DB starts empty. To test `/gps/ping` locally, insert a vehicle and a
trail first:

```bash
python -c "
from app.database import SessionLocal, init_db
from app.models import Vehicle, TrailPoint
init_db()
db = SessionLocal()
db.add(Vehicle(id='veh-1', trail_id='trail-A', is_active=True))
db.add(TrailPoint(trail_id='trail-A', sequence=0, latitude=6.3720, longitude=81.5180))
db.add(TrailPoint(trail_id='trail-A', sequence=1, latitude=6.3730, longitude=81.5190))
db.commit()
"
```

Then:

```bash
curl -X POST http://127.0.0.1:8000/gps/ping \
  -H "Content-Type: application/json" \
  -d '{"vehicle_id": "veh-1", "latitude": 6.3720, "longitude": 81.5180}'
```

## Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/health` | GET | Liveness check |
| `/gps/ping` | POST | Submit a GPS position update (driver app) |
| `/alerts` | GET | List alerts (`?active_only=true` for unacknowledged only) |
| `/alerts/{id}/acknowledge` | POST | Mark an alert as handled (dashboard) |

## What's implemented vs. what's stubbed

- **Implemented and tested:** deviation detection (nearest-trail-point
  distance via `geopy`), stationary detection (windowed cluster check
  via the APScheduler sweep job), alert persistence, alert
  acknowledgement, graceful FCM fallback when no credentials are present.
- **Stubbed for now:** trail point data is manually seeded — real trail
  geometry should come from whichever module owns park/trail mapping.
  Vehicle records are expected to be created by the booking module
  (Member 2's side) once the shared schema is live; this service only
  reads/updates them.

## Next steps against the shared schema

Once the team's Week 1 Postgres schema is live, point `DATABASE_URL` at
it and confirm the `vehicles` / `gps_pings` / `alerts` / `trail_points`
column names match `app/models.py` exactly — rename here if the shared
schema differs, rather than asking the team to match this file.
