from src.fastapi_app.services.user import _generate_tokens


def test_add_firmware(
    client,
    admin_user,
    test_session,
    devicetype,
):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_firmware = {
        "devicetype_id": devicetype.id,
        "version": "1.0.0",
        "filename": "firmware_v1.bin",
        "repo_url": "https://example.com/repo",
        "is_active": True,
    }

    response = client.post("/firmware/", headers=headers, json=new_firmware)

    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json["id"] is not None
    assert resp_json["devicetype_id"] == devicetype.id
    assert resp_json["version"] == "1.0.0"
    assert resp_json["filename"] == "firmware_v1.bin"
    assert resp_json["repo_url"] == "https://example.com/repo"
    assert resp_json["is_active"] is True


def test_add_firmware_not_admin(client, user, test_session, devicetype):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_firmware = {
        "devicetype_id": devicetype.id,
        "version": "1.0.0",
        "filename": "firmware_v1.bin",
        "repo_url": "https://example.com/repo",
        "is_active": True,
    }
    response = client.post("/firmware/", headers=headers, json=new_firmware)

    assert response.status_code == 403


def test_add_firmware_while_not_logged_in(client, devicetype):
    headers = {}

    new_firmware = {
        "devicetype_id": devicetype.id,
        "version": "2.0.0",
        "filename": "firmware_v2.bin",
        "repo_url": "https://example.com/repo2",
        "is_active": False,
    }

    response = client.post("/firmware/", headers=headers, json=new_firmware)

    assert response.status_code == 401


def test_add_firmware_with_missing_data(client, admin_user, test_session, devicetype):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    # Missing 'version' and 'filename'
    new_firmware = {"devicetype_id": devicetype.id, "is_active": True}

    response = client.post("/firmware/", headers=headers, json=new_firmware)

    assert response.status_code == 422
