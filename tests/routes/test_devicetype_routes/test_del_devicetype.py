"""
1. Delete the device type with the given ID
2. If the device type is not in the DB, return 404
3. If the user is not authenticated, return 401
/devicetype/{devicetype_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_devicetype(client, devicetype, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/devicetype/{devicetype.id}", headers=headers)

    assert response.status_code == 200


def test_delete_devicetype_not_admin(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/devicetype/{devicetype.id}", headers=headers)

    assert response.status_code == 403


def test_delete_devicetype_not_existing(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/devicetype/-1", headers=headers)

    assert response.status_code == 404


def test_delete_devicetype_not_authorized(client, devicetype):
    response = client.delete(f"/devicetype/{devicetype.id}")

    assert response.status_code == 401
