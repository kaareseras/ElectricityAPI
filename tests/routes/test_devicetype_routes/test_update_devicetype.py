"""
1. update existing device type with new data
2. if device type is missing return 404
3. if data is missing return 422
4. If the user is not authenticated, return 401
5. return the updated device type
/devicetypes/{devicetype_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_update_devicetype(client, devicetype, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_devicetype = {
        "id": devicetype.id,
        "name": "Smart Meter X",
        "hw_version": "HW-2.0",
        "sw_version": "SW-3.1",
        "sw_date": "2024-06-01T00:00:00",
    }

    response = client.put(f"/devicetype/{devicetype.id}", headers=headers, json=updated_devicetype)

    assert response.status_code == 200
    assert response.json()["id"] == updated_devicetype["id"]
    assert response.json()["name"] == updated_devicetype["name"]
    assert response.json()["hw_version"] == updated_devicetype["hw_version"]
    assert response.json()["sw_version"] == updated_devicetype["sw_version"]
    assert response.json()["sw_date"] == updated_devicetype["sw_date"]


def test_update_devicetype_not_admin(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_devicetype = {
        "id": devicetype.id,
        "name": "Smart Meter X",
        "hw_version": "HW-2.0",
        "sw_version": "SW-3.1",
        "sw_date": "2024-06-01T00:00:00",
    }

    response = client.put(f"/devicetype/{devicetype.id}", headers=headers, json=updated_devicetype)

    assert response.status_code == 403


def test_update_devicetype_while_not_logged_in(client, devicetype):
    response = client.put(f"/devicetype/{devicetype.id}")
    assert response.status_code == 401


def test_update_devicetype_with_missing_data(client, devicetype, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_devicetype = {
        "id": devicetype.id,
        # "name": "Smart Meter X",  # Missing required field
        "hw_version": "HW-2.0",
        "sw_version": "SW-3.1",
        "sw_date": "2024-06-01",
    }

    response = client.put(f"/devicetype/{devicetype.id}", headers=headers, json=updated_devicetype)
    assert response.status_code == 422
