"""
1. Successfully add a new charge to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/chargers/{charger_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_charge(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_charge = {
        "chargeowner_id": chargeowner.id,
        "charge_type": "Type1",
        "charge_type_code": "Code1",
        "note": "Test note",
        "description": "Test description",
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "price1": 0.1,
        "price2": 0.2,
        "price3": 0.3,
        "price4": 0.4,
        "price5": 0.5,
        "price6": 0.6,
        "price7": 0.7,
        "price8": 0.8,
        "price9": 0.9,
        "price10": 1.0,
        "price11": 1.1,
        "price12": 1.2,
        "price13": 1.3,
        "price14": 1.4,
        "price15": 1.5,
        "price16": 1.6,
        "price17": 1.7,
        "price18": 1.8,
        "price19": 1.9,
        "price20": 2.0,
        "price21": 2.1,
        "price22": 2.2,
        "price23": 2.3,
        "price24": 2.4,
    }

    response = client.post("/charge/", headers=headers, json=new_charge)

    assert response.status_code == 200
    assert response.json()["id"] is not None


def test_add_charge_within_existing_charge_periode(client, chargeowner, charge, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_charge = {
        "chargeowner_id": chargeowner.id,
        "charge_type": "Type1",
        "charge_type_code": "Code1",
        "note": "Test note",
        "description": "Test description",
        "valid_from": charge.valid_from.strftime("%Y-%m-%dT%H:%M:%S"),
        "valid_to": charge.valid_to.strftime("%Y-%m-%dT%H:%M:%S"),
        "price1": 0.1,
        "price2": 0.2,
        "price3": 0.3,
        "price4": 0.4,
        "price5": 0.5,
        "price6": 0.6,
        "price7": 0.7,
        "price8": 0.8,
        "price9": 0.9,
        "price10": 1.0,
        "price11": 1.1,
        "price12": 1.2,
        "price13": 1.3,
        "price14": 1.4,
        "price15": 1.5,
        "price16": 1.6,
        "price17": 1.7,
        "price18": 1.8,
        "price19": 1.9,
        "price20": 2.0,
        "price21": 2.1,
        "price22": 2.2,
        "price23": 2.3,
        "price24": 2.4,
    }

    response = client.post("/charge/", headers=headers, json=new_charge)

    assert response.status_code == 404


def test_add_charge_non_existing_chargeowner(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_charge = {
        "chargeowner_id": chargeowner.id + 1,
        "charge_type": "Type1",
        "charge_type_code": "Code1",
        "note": "Test note",
        "description": "Test description",
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "price1": 0.1,
        "price2": 0.2,
        "price3": 0.3,
        "price4": 0.4,
        "price5": 0.5,
        "price6": 0.6,
        "price7": 0.7,
        "price8": 0.8,
        "price9": 0.9,
        "price10": 1.0,
        "price11": 1.1,
        "price12": 1.2,
        "price13": 1.3,
        "price14": 1.4,
        "price15": 1.5,
        "price16": 1.6,
        "price17": 1.7,
        "price18": 1.8,
        "price19": 1.9,
        "price20": 2.0,
        "price21": 2.1,
        "price22": 2.2,
        "price23": 2.3,
        "price24": 2.4,
    }

    response = client.post("/charge/", headers=headers, json=new_charge)

    assert response.status_code == 404


def test_add_charge_while_not_logged_in(client, chargeowner, test_session):
    headers = {}

    new_charge = {
        "chargeowner_id": chargeowner.id,
        "charge_type": "Type1",
        "charge_type_code": "Code1",
        "note": "Test note",
        "description": "Test description",
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "price1": 0.1,
        "price2": 0.2,
        "price3": 0.3,
        "price4": 0.4,
        "price5": 0.5,
        "price6": 0.6,
        "price7": 0.7,
        "price8": 0.8,
        "price9": 0.9,
        "price10": 1.0,
        "price11": 1.1,
        "price12": 1.2,
        "price13": 1.3,
        "price14": 1.4,
        "price15": 1.5,
        "price16": 1.6,
        "price17": 1.7,
        "price18": 1.8,
        "price19": 1.9,
        "price20": 2.0,
        "price21": 2.1,
        "price22": 2.2,
        "price23": 2.3,
        "price24": 2.4,
    }

    response = client.post("/charge/", headers=headers, json=new_charge)

    assert response.status_code == 401


def test_add_charge_with_missing_data(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_charge = {
        "chargeowner_id": chargeowner.id,
        "charge_type": "Type1",
        "charge_type_code": "Code1",
        "note": "Test note",
        "description": "Test description",
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        # Missing price1
    }

    response = client.post("/charge/", headers=headers, json=new_charge)

    assert response.status_code == 422
