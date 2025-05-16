"""
1. Delete the charge with the given ID
2. If the charge is not in the DB, return 404
3. If the user is not authenticated, return 401
/charge/{charge_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_charge(client, charge, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/charge/{charge.id}", headers=headers)

    assert response.status_code == 200


def test_delete_charge_not_existing(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/charge/-1", headers=headers)

    assert response.status_code == 404


def test_delete_charge_not_authorized(client, charge):
    response = client.delete(f"/charge/{charge.id}")

    assert response.status_code == 401
