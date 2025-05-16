"""
1. Delete the spot price with the given ID
2. If the spot price is not in the DB, return 404
3. If the user is not authenticated, return 401
/spotprice/{spotprice_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_delete_spotprice(client, spotprice, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete(f"/spotprice/{spotprice.id}", headers=headers)

    assert response.status_code == 200


def test_delete_spotprice_not_existing(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.delete("/spotprice/-1", headers=headers)

    assert response.status_code == 404


def test_delete_spotprice_not_authorized(client, spotprice):
    response = client.delete(f"/spotprice/{spotprice.id}")

    assert response.status_code == 401
