"""
1. Get a list of all charge owners without the current status and power
2. Only get the charge owners details if the user is authenticated
3. Get a 404 not found if there are no charge owners in the DB
/chargeowners/{chargeowner_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_fetch_chargeowners(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/chargeowner/", headers=headers)

    assert response.status_code == 200


def test_fetch_chargeowners_while_not_logged_in(client, chargeowner):
    response = client.get("/chargeowner/")

    assert response.status_code == 401


def test_fetch_chargeowners_with_no_chargers_in_DB(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/chargeowner/", headers=headers)

    assert response.status_code == 200
    assert response.json() == []
