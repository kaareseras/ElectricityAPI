"""
Tests for hardware routes.
Functions:
1. Test fetching a hardware by ID.
2. Test fetching all hardware.
3. Test fetching hardware with an invalid ID.
4. Test fetching hardware without being logged in.
"""

from src.fastapi_app.services.user import _generate_tokens

# Test for fetching hardware by ID


def test_fetch_hardware(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/hardware/{hardware.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == hardware.id


# Test for fetching all hardware


def test_fetch_all_hardware(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/hardware", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


# Test for fetching hardware with an invalid ID


def test_fetch_hardware_with_wrong_id(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/hardware/-1", headers=headers)

    assert response.status_code == 404


# Test for fetching hardware without being logged in


def test_fetch_hardware_while_not_logged_in(client, hardware):
    response = client.get(f"/hardware/{hardware.id}")

    assert response.status_code == 401
