"""
1. Successfully add a new device to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/devices/{device_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_device(client, admin_user, test_session, devicetype):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = "123e4567-e89b-12d3-a456-426614174000"
    json = {"uuid": uuid, "devicetype_id": devicetype.id}

    response = client.post("/device", headers=headers, json=json)

    assert response.status_code == 200
    assert response.json()["uuid"] == uuid
    assert response.json()["name"] == uuid
    assert response.json()["devicetype_id"] == devicetype.id


def test_add_device_with_existing_uuid(client, device, admin_user, test_session, devicetype):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = device.uuid

    json = {"uuid": uuid, "devicetype_id": devicetype.id}

    response = client.post("/device", headers=headers, json=json)

    assert response.status_code == 404
    assert response.json()["detail"] == "Device already exists."


def test_add_device_while_not_logged_in(client, test_session, devicetype):
    headers = {}

    uuid = "123e4567-e89b-12d3-a456-426614174000"
    json = {"uuid": uuid, "devicetype_id": devicetype.id}

    response = client.post("/device", headers=headers, json=json)

    assert response.status_code == 401


def test_add_device_while_not_admin(client, user, test_session, devicetype):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = "123e4567-e89b-12d3-a456-426614174000"
    json = {"uuid": uuid, "devicetype_id": devicetype.id}

    response = client.post("/device", headers=headers, json=json)

    assert response.status_code == 403
