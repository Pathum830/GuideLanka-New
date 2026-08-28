"""Unit tests for the pure geometry functions -- no DB, no FastAPI needed.

These are the fast, first-line tests: run them constantly while tweaking
threshold values or the distance logic.
"""
from app.services.detection import nearest_distance_to_trail, is_cluster_stationary

# Roughly Yala National Park area, Sri Lanka -- arbitrary but realistic coords.
TRAIL = [
    (6.3720, 81.5180),
    (6.3730, 81.5190),
    (6.3740, 81.5200),
]


def test_on_trail_is_zero_ish():
    # A point essentially on the trail should be very close to 0m.
    distance = nearest_distance_to_trail((6.3720, 81.5180), TRAIL)
    assert distance < 1


def test_far_from_trail_exceeds_threshold():
    # ~0.01 degrees latitude is roughly 1.1km -- well past 200m.
    distance = nearest_distance_to_trail((6.3820, 81.5180), TRAIL)
    assert distance > 200


def test_no_trail_points_returns_zero():
    # No mapped trail for this vehicle -- can't evaluate, so don't false-trigger.
    distance = nearest_distance_to_trail((6.3720, 81.5180), [])
    assert distance == 0.0


def test_cluster_within_radius_is_stationary():
    positions = [
        (6.3720, 81.5180),
        (6.37201, 81.51801),
        (6.37199, 81.51799),
    ]
    assert is_cluster_stationary(positions, radius_m=15) is True


def test_cluster_spread_out_is_not_stationary():
    positions = [
        (6.3720, 81.5180),
        (6.3730, 81.5190),  # ~1.4km away -- clearly moving
    ]
    assert is_cluster_stationary(positions, radius_m=15) is False


def test_single_position_is_not_enough_to_call_stationary():
    assert is_cluster_stationary([(6.3720, 81.5180)], radius_m=15) is False
