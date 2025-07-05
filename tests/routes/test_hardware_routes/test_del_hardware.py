"""
1. Delete the hardware with the given ID
2. If the hardware is not in the DB, return 404
3. If the user is not authenticated, return 401
/hardware/{hardware_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_hardware(client, hardware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/hardware/{hardware.id}", headers=headers)

    assert response.status_code == 200


def test_delete_hardware_not_admin(client, hardware, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/hardware/{hardware.id}", headers=headers)

    assert response.status_code == 403


def test_delete_hardware_not_existing(client, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/hardware/-1", headers=headers)

    assert response.status_code == 404


def test_delete_hardware_not_authorized(client, hardware):
    response = client.delete(f"/hardware/{hardware.id}")

    assert response.status_code == 401
