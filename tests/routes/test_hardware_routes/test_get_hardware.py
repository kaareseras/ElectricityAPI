"""
Tests for hardware routes.

Test cases:
1. Fetch hardware by ID as admin (should succeed).
2. Fetch hardware by ID as non-admin (should fail with 403).
3. Fetch hardware by DeviceType ID as admin (should succeed).
4. Fetch hardware by DeviceType ID as non-admin (should fail with 403).
5. Fetch all hardware as admin (should succeed).
6. Fetch all hardware as non-admin (should fail with 403).
7. Fetch all hardware when no hardware in DB as non-admin (should fail with 403).
8. Fetch hardware with invalid ID as non-admin (should fail with 403).
9. Fetch hardware by ID without authentication (should fail with 401).
10. Fetch all hardware without authentication (should fail with 401).
"""

from src.fastapi_app.services.user import _generate_tokens

# Test for fetching hardware by ID


def test_fetch_hardware(client, hardware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/hardware/{hardware.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == hardware.id


def test_fetch_hardware_not_admin(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/hardware/{hardware.id}", headers=headers)

    assert response.status_code == 403

    # Test for fetching hardware by DeviceType ID


def test_fetch_hardware_by_device(client, devicetype, hardware, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/hardware/by-devicetype/{devicetype.id}", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == hardware.id


def test_fetch_hardware_by_device_not_admin(client, devicetype, hardware, firmware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/hardware/by-devicetype/{devicetype.id}", headers=headers)

    assert response.status_code == 403


# Test for fetching all hardware


def test_fetch_all_hardware(client, hardware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/hardware", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_fetch_all_hardware_no_in_db(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/hardware", headers=headers)

    assert response.status_code == 403


def test_fetch_all_hardware_not_admin(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/hardware", headers=headers)

    assert response.status_code == 403


# Test for fetching hardware with an invalid ID


def test_fetch_hardware_with_wrong_id(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/hardware/-1", headers=headers)

    assert response.status_code == 403


# Test for fetching hardware without being logged in


def test_fetch_hardware_while_not_logged_in(client, hardware):
    response = client.get(f"/hardware/{hardware.id}")

    assert response.status_code == 401


def test_fetch_all_hardware_while_not_logged_in(client, hardware):
    response = client.get("/hardware")

    assert response.status_code == 401
