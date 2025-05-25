"""
1. Successfully add a new charge owner to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/chargers/{charger_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_charger(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_chargeowner = {
        "glnnumber": "5790000705689",
        "compagny": "Hurup Elværk Net A/S",
        "chargetype": "D03",
        "chargetypecode": "DT_C_01",
    }

    response = client.post("/chargeowner/", headers=headers, json=new_chargeowner)

    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["compagny"] == "Hurup Elværk Net A/S"


def test_add_chargeowner_while_not_logged_in(client, test_session):
    headers = {}

    new_chargeowner = {
        "glnnumber": "5790000705689",
        "compagny": "Radius Elnet A/S",
        "chargetype": "DT_C_01",
        "chargetypecode": "D03",
    }

    response = client.post("/chargeowner/", headers=headers, json=new_chargeowner)

    assert response.status_code == 401


def test_add_chargeowner_with_missing_data(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_chargeowner = {
        "name": "Radius",
        "glnnumber": "5790000705689",
        "compagny": "Radius Elnet A/S",
        "type": "DT_C_01",
    }

    response = client.post("/chargeowner/", headers=headers, json=new_chargeowner)

    assert response.status_code == 422
