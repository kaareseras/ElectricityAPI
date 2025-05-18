"""
1. update existing charge owner with new data
2. if charge owner is missing return 404
3. if data is missing return 422
4. If the user is not authenticated, return 401
5. return the updated charge owner with HA current state and power
/chargeowners/{chargeowner_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_update_chargeowner(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_chargeowner = {
        "id": chargeowner.id,
        "name": "Radius updated",
        "glnnumber": "5790000705689",
        "company": "Radius Elnet A/S",
        "type": "DT_C_01",
        "chargetype": "D03",
        "is_active": False,
    }

    response = client.put(f"/chargeowner/{chargeowner.id}", headers=headers, json=updated_chargeowner)

    assert response.status_code == 200
    assert response.json()["id"] is not None
    assert response.json()["name"] == updated_chargeowner["name"]
    assert response.json()["glnnumber"] == updated_chargeowner["glnnumber"]
    assert response.json()["company"] == updated_chargeowner["company"]
    assert response.json()["type"] == updated_chargeowner["type"]
    assert response.json()["chargetype"] == updated_chargeowner["chargetype"]
    assert response.json()["is_active"] == updated_chargeowner["is_active"]


def test_update_chargeowner_while_not_logged_in(client, chargeowner):
    response = client.put(f"/chargeowner/{chargeowner.id}")

    assert response.status_code == 401


def test_add_chargeowner_with_missing_data(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    updated_chargeowner = {
        "id": chargeowner.id,
        "name": "Radius updated",
        "glnnumber": "5790000705689",
        "company": "Radius Elnet A/S",
        "type": "DT_C_01",
    }

    response = client.put(f"/chargeowner/{chargeowner.id}", headers=headers, json=updated_chargeowner)

    assert response.status_code == 422
