"""
Tests for device routes.
Functions:
1. Test fetching a device by ID.
2. Test fetching all devices.
3. Test fetching today's device.
4. Test fetching a device for a specific date.
5. Test fetching a device for a specific date when no device is found.
6. Test fetching a device with an invalid ID.
7. Test fetching a device without being logged in.
"""

from src.fastapi_app.services.user import _generate_tokens


# Test for fetching device by ID
def test_fetch_device(client, device, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/device/{device.uuid}", headers=headers)

    assert response.status_code == 200
    assert response.json()["uuid"] == device.uuid


# Test for fetching all devices
def test_fetch_all_devices(client, device, device2, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/device/all", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2

    for dev in response.json():
        assert dev.get("name") is not None
        assert dev.get("user_id") is not None


# Test for fetching all devices with non admin user
def test_fetch_all_devices_not_admin(client, device, device2, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/device/all", headers=headers)

    assert response.status_code == 403


# Test for fetching all devices for specific user
def test_fetch_all_devices_for_user(client, device, device2, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/device", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2

    for dev in response.json():
        assert dev.get("name") is not None
        assert dev.get("user_id") is not None


# Test for fetching device with an invalid ID


def test_fetch_device_with_wrong_id(client, device, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/device/uuid/-1", headers=headers)

    assert response.status_code == 404


# Test for fetching device without being logged in


def test_fetch_device_while_not_logged_in(client, device):
    response = client.get(f"/device/{device.uuid}")

    assert response.status_code == 401
