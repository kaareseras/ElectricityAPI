"""
1. Delete the tarif with the given ID
2. If the tarif is not in the DB, return 404
3. If the user is not authenticated, return 401
/tarif/{tarif_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_tarif(client, tarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/tarif/{tarif.id}", headers=headers)

    assert response.status_code == 200


def test_delete_tarif_not_existing(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/tarif/-1", headers=headers)

    assert response.status_code == 404


def test_delete_tarif_not_authorized(client, tarif):
    response = client.delete(f"/tarif/{tarif.id}")

    assert response.status_code == 401
