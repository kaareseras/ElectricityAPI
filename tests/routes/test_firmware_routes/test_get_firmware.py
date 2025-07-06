"""
Tests for firmware routes.
Functions:
1. Test fetching a firmware by ID.
2. Test fetching all firmwares.
3. Test fetching firmware with an invalid ID.
4. Test fetching firmware without being logged in.
"""

from src.fastapi_app.services.user import _generate_tokens


# Test for fetching firmware by ID
def test_fetch_firmware(client, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/firmware/{firmware.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == firmware.id


def test_fetch_firmware_not_admin(client, firmware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/firmware/{firmware.id}", headers=headers)

    assert response.status_code == 403


# Test for fetching all firmwares


def test_fetch_all_firmwares(client, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/firmware", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_fetch_all_firmwares_non_in_db(client, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/firmware", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 0


def test_fetch_all_firmwares_not_admin(client, firmware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/firmware", headers=headers)

    assert response.status_code == 403


# Test for fetching firmware with an invalid ID


def test_fetch_firmware_with_wrong_id(client, firmware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/firmware/-1", headers=headers)

    assert response.status_code == 403


# Test for fetching firmware without being logged in


def test_fetch_firmware_while_not_logged_in(client, firmware):
    response = client.get(f"/firmware/{firmware.id}")

    assert response.status_code == 401
