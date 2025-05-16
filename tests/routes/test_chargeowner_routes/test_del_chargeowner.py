"""
1. Delete the charge owner with the given ID
2. If the charge owner is not in the DB, return 404
3. If the user is not authenticated, return 401
/chargeowners/{chargeowner_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_chargeowner(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/chargeowner/{chargeowner.id}", headers=headers)

    assert response.status_code == 200


def test_delete_chargeowner_not_existing(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/chargeowner/-1", headers=headers)

    assert response.status_code == 404


def test_fetch_chargeowner_not_authorised(client, chargeowner):
    response = client.delete(f"/chargeowner/{chargeowner.id}")

    assert response.status_code == 401
