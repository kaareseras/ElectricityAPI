"""
1. Get Charge Owner details
2. If requesting a Charge Owner not in DB return 404
3. If the user is not authenticated, return 401
/chargeowners/{chargeowner_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_fetch_chargeowner(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/chargeowner/{chargeowner.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == chargeowner.id


def test_fetch_chargeowner_with_wrong_id(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/chargeowner/-1", headers=headers)

    assert response.status_code == 404


def test_fetch_chargeowner_while_not_logged_in(client, chargeowner):
    response = client.get(f"/chargeowner/{chargeowner.id}")

    assert response.status_code == 401
