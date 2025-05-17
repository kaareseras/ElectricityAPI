"""
1. Successfully add a new device to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/devices/{device_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_device(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = "123e4567-e89b-12d3-a456-426614174000"

    new_device = {"uuid": uuid}

    response = client.post("/device/", headers=headers, json=new_device)

    assert response.status_code == 200
    assert response.json()["uuid"] == uuid
    assert response.json()["name"] == uuid
    assert response.json()["user_id"] == user.id


def test_add_device_with_existing_uuid(client, device, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    new_device = {"uuid": device.uuid}  # re-using existing UUID

    response = client.post("/device/", headers=headers, json=new_device)

    assert response.status_code == 404
    assert response.json()["detail"] == "Device already exists."


def test_add_device_while_not_logged_in(client, test_session):
    headers = {}

    new_device = {"uuid": "123e4567-e89b-12d3-a456-426614174000"}

    response = client.post("/device/", headers=headers, json=new_device)

    assert response.status_code == 401


def test_add_device_with_missing_data(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_device = {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        # Missing chargeowner_id
        "PriceArea": "Area1",
        "Config": '{"setting": "value"}',
        "last_activity": "2025-01-04T00:00:00",
    }

    response = client.post("/device/", headers=headers, json=new_device)

    assert response.status_code == 422
