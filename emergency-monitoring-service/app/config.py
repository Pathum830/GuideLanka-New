"""Central place to load and expose configuration.

Every other module should import settings from here rather than calling
os.getenv() directly, so there is exactly one source of truth for config.
"""
import os
from dotenv import load_dotenv

load_dotenv()


def _bool_env(name: str, default: bool) -> bool:
    val = os.getenv(name)
    if val is None:
        return default
    return val.strip().lower() in ("1", "true", "yes", "on")


class Settings:
    # Falls back to a local SQLite file so the service is runnable
    # before the shared Postgres instance is wired up.
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

    FIREBASE_CREDENTIALS_PATH: str = os.getenv(
        "FIREBASE_CREDENTIALS_PATH", "./firebase-service-account.json"
    )
    FCM_ALERT_TOPIC: str = os.getenv("FCM_ALERT_TOPIC", "park-authority-alerts")

    STATIONARY_THRESHOLD_MINUTES: int = int(
        os.getenv("STATIONARY_THRESHOLD_MINUTES", "10")
    )
    STATIONARY_RADIUS_METERS: float = float(
        os.getenv("STATIONARY_RADIUS_METERS", "15")
    )
    DEVIATION_THRESHOLD_METERS: float = float(
        os.getenv("DEVIATION_THRESHOLD_METERS", "200")
    )
    SWEEP_INTERVAL_MINUTES: int = int(os.getenv("SWEEP_INTERVAL_MINUTES", "1"))


settings = Settings()
