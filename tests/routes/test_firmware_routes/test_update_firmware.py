"""
1. update existing firmware with new data
2. if firmware is missing return 404
3. if data is missing return 422
4. If the user is not authenticated, return 401
5. return the updated firmware
/firmware/{firmware_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_update_firmware(client, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_firmware = {
        "id": firmware.id,
        "devicetype_id": firmware.devicetype_id,
        "version": "2.0.0",
        "filename": "firmware_v2.bin",
        "repo_url": "https://repo.example.com/firmware_v2",
        "is_active": True,
    }

    response = client.put(f"/firmware/{firmware.id}", headers=headers, json=updated_firmware)

    assert response.status_code == 200
    assert response.json()["id"] == updated_firmware["id"]
    assert response.json()["version"] == updated_firmware["version"]
    assert response.json()["filename"] == updated_firmware["filename"]
    assert response.json()["repo_url"] == updated_firmware["repo_url"]
    assert response.json()["is_active"] == updated_firmware["is_active"]


def test_update_firmware_not_admin(client, firmware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_firmware = {
        "id": firmware.id,
        "devicetype_id": firmware.devicetype_id,
        "version": "2.0.0",
        "filename": "firmware_v2.bin",
        "repo_url": "https://repo.example.com/firmware_v2",
        "is_active": True,
    }

    response = client.put(f"/firmware/{firmware.id}", headers=headers, json=updated_firmware)

    assert response.status_code == 403


def test_update_firmware_while_not_logged_in(client, firmware):
    response = client.put(f"/firmware/{firmware.id}")
    assert response.status_code == 401


def test_update_firmware_with_missing_data(client, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_firmware = {
        "id": firmware.id,
        "devicetype_id": firmware.devicetype_id,
        # "version": "2.0.0",  # Missing required field
        "filename": "firmware_v2.bin",
        "repo_url": "https://repo.example.com/firmware_v2",
        "is_active": True,
    }

    response = client.put(f"/firmware/{firmware.id}", headers=headers, json=updated_firmware)
    assert response.status_code == 422
