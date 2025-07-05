from src.fastapi_app.services.user import _generate_tokens


def test_add_hardware(
    client,
    admin_user,
    test_session,
    devicetype,
):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_hardware = {
        "devicetype_id": devicetype.id,
        "version": "1.0.0",
        "name": "Main Board",
        "description": "Main control board for device",
        "is_active": True,
    }

    response = client.post("/hardware/", headers=headers, json=new_hardware)

    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["id"] is not None
    assert resp_json["devicetype_id"] == devicetype.id
    assert resp_json["version"] == "1.0.0"
    assert resp_json["name"] == "Main Board"
    assert resp_json["description"] == "Main control board for device"
    assert resp_json["is_active"] is True


def test_add_hardware_not_admin(client, user, test_session, devicetype):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_hardware = {
        "devicetype_id": devicetype.id,
        "version": "1.0.0",
        "name": "Main Board",
        "description": "Main control board for device",
        "is_active": True,
    }
    response = client.post("/hardware/", headers=headers, json=new_hardware)

    assert response.status_code == 403


def test_add_hardware_while_not_logged_in(client, devicetype):
    headers = {}

    new_hardware = {
        "devicetype_id": devicetype.id,
        "version": "2.0.0",
        "name": "Expansion Board",
        "description": "Expansion board for additional features",
        "is_active": False,
    }

    response = client.post("/hardware/", headers=headers, json=new_hardware)

    assert response.status_code == 401


def test_add_hardware_with_missing_data(client, admin_user, test_session, devicetype):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # Missing 'version' and 'name'
    new_hardware = {"devicetype_id": devicetype.id, "is_active": True}

    response = client.post("/hardware/", headers=headers, json=new_hardware)

    assert response.status_code == 422
