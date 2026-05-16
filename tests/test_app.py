import os
import sys
import pytest

# Ensure src is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import activities, get_activities, signup_for_activity, remove_participant
from fastapi import HTTPException


def test_get_activities():
    acts = get_activities()
    assert isinstance(acts, dict)
    assert "Chess Club" in acts


def test_signup_and_remove():
    activity = "Chess Club"
    email = "tester@example.com"

    # Clean up if present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = signup_for_activity(activity, email)
    assert "Signed up" in resp["message"]
    assert email in activities[activity]["participants"]

    resp2 = remove_participant(activity, email)
    assert "Removed" in resp2["message"]
    assert email not in activities[activity]["participants"]


def test_signup_nonexistent_activity_raises():
    with pytest.raises(HTTPException) as exc:
        signup_for_activity("No Such Activity", "a@b.com")
    assert exc.value.status_code == 404


def test_signup_duplicate_raises():
    activity = "Programming Class"
    # use an existing participant
    email = activities[activity]["participants"][0]
    with pytest.raises(HTTPException) as exc:
        signup_for_activity(activity, email)
    assert exc.value.status_code == 400


def test_remove_nonexistent_participant_raises():
    activity = "Chess Club"
    email = "not-a-participant@example.com"
    # ensure it's not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    with pytest.raises(HTTPException) as exc:
        remove_participant(activity, email)
    assert exc.value.status_code == 404
