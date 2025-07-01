from src.fastapi_app.services.user import _generate_tokens


def test_add_devicetype(client, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_devicetype = {"name": "SensorX", "hw_version": "1.0", "sw_version": "2.0", "sw_date": "2025-01-04T00:00:00"}

    response = client.post("/devicetype/", headers=headers, json=new_devicetype)

    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["name"] == "SensorX"
    assert response.json()["hw_version"] == "1.0"
    assert response.json()["sw_version"] == "2.0"
    assert response.json()["sw_date"] == "2025-01-04T00:00:00"


def test_add_devicetype_not_admin(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_devicetype = {"name": "SensorX", "hw_version": "1.0", "sw_version": "2.0", "sw_date": "2025-01-04T00:00:00"}

    response = client.post("/devicetype/", headers=headers, json=new_devicetype)

    assert response.status_code == 403


def test_add_devicetype_with_existing_name(client, devicetype, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_devicetype = {"name": devicetype.name, "hw_version": "1.0", "sw_version": "2.0", "sw_date": "2025-01-04"}

    response = client.post("/devicetype/", headers=headers, json=new_devicetype)

    assert response.status_code == 400


def test_add_devicetype_while_not_logged_in(client, test_session):
    headers = {}

    new_devicetype = {"name": "SensorY", "hw_version": "1.1", "sw_version": "2.1", "sw_date": "2025-01-05"}

    response = client.post("/devicetype/", headers=headers, json=new_devicetype)

    assert response.status_code == 401


def test_add_devicetype_with_missing_data(client, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_devicetype = {
        # Missing 'name'
        "hw_version": "1.2",
        "sw_version": "2.2",
        "sw_date": "2025-01-06",
    }

    response = client.post("/devicetype/", headers=headers, json=new_devicetype)

    assert response.status_code == 422
