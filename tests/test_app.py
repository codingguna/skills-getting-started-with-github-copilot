from fastapi.testclient import TestClient
import pytest

from src.app import app, activities


client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # Basic sanity checks
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser_ci@example.com"

    # Ensure clean starting state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_signup_activity_not_found():
    resp = client.post("/activities/NoSuchActivity/signup?email=x@example.com")
    assert resp.status_code == 404


def test_unregister_not_signed_up():
    activity = "Chess Club"
    email = "not-signed-up@example.com"
    # Ensure email is not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 404
