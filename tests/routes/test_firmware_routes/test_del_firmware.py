"""
1. Delete the firmware with the given ID
2. If the firmware is not in the DB, return 404
3. If the user is not authenticated, return 401
/firmware/{firmware_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_firmware(client, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/firmware/{firmware.id}", headers=headers)

    assert response.status_code == 200


def test_delete_firmware_not_admin(client, firmware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/firmware/{firmware.id}", headers=headers)

    assert response.status_code == 403


def test_delete_firmware_not_existing(client, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/firmware/-1", headers=headers)

    assert response.status_code == 404


def test_delete_firmware_not_authorized(client, firmware):
    response = client.delete(f"/firmware/{firmware.id}")

    assert response.status_code == 401
