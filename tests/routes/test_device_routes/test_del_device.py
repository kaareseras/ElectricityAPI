"""
1. Delete the device with the given UUID
2. If the device is not in the DB, return 404
3. If the user is not authenticated, return 401
/device/{device_uuid}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_device(client, device, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/device/{device.uuid}", headers=headers)

    assert response.status_code == 200


def test_delete_device_not_existing(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/device/non-existing-uuid", headers=headers)

    assert response.status_code == 404


def test_delete_device_not_authorized(client, device):
    response = client.delete(f"/device/{device.uuid}")

    assert response.status_code == 401
