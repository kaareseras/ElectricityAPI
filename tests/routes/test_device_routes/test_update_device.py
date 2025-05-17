"""
1. update existing charge owner with new data
2. if charge owner is missing return 404
3. if data is missing return 422
4. If the user is not authenticated, return 401
5. return the updated charge owner with HA current state and power
/chargeowners/{chargeowner_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_update_device(client, device, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_device = {
        "uuid": device.uuid,
        "name": "Updated Device Name",
        "chargeowner_id": device.chargeowner_id,
        "PriceArea": "DK2",
        "Config": '{"setting": "new_value"}',
    }

    response = client.put(f"/device/{device.uuid}", headers=headers, json=updated_device)

    assert response.status_code == 200
    assert response.json()["uuid"] is not None


def test_update_device_while_not_logged_in(client, device):
    response = client.put(f"/device/{device.uuid}")

    assert response.status_code == 401


def test_update_device_with_missing_data(client, device, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_device = {"uuid": device.uuid, "chargeowner_id": device.chargeowner_id, "PriceArea": "DK2"}

    response = client.put(f"/device/{device.uuid}", headers=headers, json=updated_device)

    assert response.status_code == 422
