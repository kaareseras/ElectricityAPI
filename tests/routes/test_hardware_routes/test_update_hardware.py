"""
1. update existing hardware with new data
2. if hardware is missing return 404
3. if data is missing return 422
4. If the user is not authenticated, return 401
5. return the updated hardware
/hardware/{hardware_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_update_hardware(client, hardware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_hardware = {
        "id": hardware.id,
        "devicetype_id": hardware.devicetype_id,
        "version": "2.0",
        "name": "Smart Meter HW X",
        "description": "A smart meter hardware",
        "is_active": True,
    }

    response = client.put(f"/hardware/{hardware.id}", headers=headers, json=updated_hardware)

    assert response.status_code == 200
    assert response.json()["id"] == updated_hardware["id"]
    assert response.json()["name"] == updated_hardware["name"]
    assert response.json()["description"] == updated_hardware["description"]
    assert response.json()["version"] == updated_hardware["version"]
    assert response.json()["is_active"] == updated_hardware["is_active"]
    assert response.json()["devicetype_id"] == updated_hardware["devicetype_id"]


def test_update_hardware_not_admin(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_hardware = {
        "id": hardware.id,
        "devicetype_id": hardware.devicetype_id,
        "version": "2.0",
        "name": "Smart Meter HW X",
        "description": "A smart meter hardware",
        "is_active": True,
    }

    response = client.put(f"/hardware/{hardware.id}", headers=headers, json=updated_hardware)

    assert response.status_code == 403


def test_update_hardware_while_not_logged_in(client, hardware):
    response = client.put(f"/hardware/{hardware.id}")
    assert response.status_code == 401


def test_update_hardware_with_missing_data(client, hardware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_hardware = {
        "id": hardware.id,
        "devicetype_id": hardware.devicetype_id,
        # "version": "2.0",  # Missing required field
        "name": "Smart Meter HW X",
        "description": "A smart meter hardware",
        "is_active": True,
    }

    response = client.put(f"/hardware/{hardware.id}", headers=headers, json=updated_hardware)
    assert response.status_code == 422
