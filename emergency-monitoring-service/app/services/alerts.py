"""Alert persistence + push dispatch (FR10).

Firebase is initialized lazily and defensively: if no credentials file is
present (e.g. running locally before the Firebase project is shared with
you), alerts are still saved to the DB and just logged instead of pushed.
This keeps the service runnable end-to-end without blocking on Firebase
setup.
"""
import logging
import os

from sqlalchemy.orm import Session

from app.config import settings
from app.models import Alert, Vehicle

logger = logging.getLogger("emergency_monitoring.alerts")

_firebase_app = None
_firebase_unavailable_reason: str | None = None


def _get_firebase_app():
    global _firebase_app, _firebase_unavailable_reason
    if _firebase_app is not None or _firebase_unavailable_reason is not None:
        return _firebase_app

    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        _firebase_unavailable_reason = (
            f"no credentials file at {settings.FIREBASE_CREDENTIALS_PATH}"
        )
        logger.warning(
            "FCM disabled (%s) -- alerts will be logged, not pushed.",
            _firebase_unavailable_reason,
        )
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials

        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        _firebase_app = firebase_admin.initialize_app(cred)
        return _firebase_app
    except Exception as exc:  # noqa: BLE001 -- log and degrade gracefully
        _firebase_unavailable_reason = str(exc)
        logger.exception("Failed to initialize Firebase -- falling back to log-only alerts.")
        return None


def _push_fcm(alert: Alert) -> bool:
    """Best-effort FCM push. Returns True if actually sent."""
    app = _get_firebase_app()
    if app is None:
        return False

    from firebase_admin import messaging

    message = messaging.Message(
        notification=messaging.Notification(
            title=f"{alert.alert_type.upper()} — Vehicle {alert.vehicle_id}",
            body=alert.detail,
        ),
        data={
            "vehicle_id": alert.vehicle_id,
            "alert_type": alert.alert_type,
            "alert_id": alert.id,
        },
        topic=settings.FCM_ALERT_TOPIC,
    )
    messaging.send(message)
    return True


def trigger_alert(db: Session, vehicle_id: str, alert_type: str, detail: str) -> Alert:
    """Persist an alert and attempt to push it. Always returns the saved record."""
    record = Alert(vehicle_id=vehicle_id, alert_type=alert_type, detail=detail)
    db.add(record)
    db.commit()
    db.refresh(record)

    sent = False
    try:
        sent = _push_fcm(record)
    except Exception:  # noqa: BLE001 -- never let a push failure lose the alert
        logger.exception("FCM push failed for alert %s", record.id)

    if not sent:
        logger.info("ALERT [%s] vehicle=%s: %s", alert_type, vehicle_id, detail)

    return record
