"""
1. Successfully add a new tax to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/taxes/{tax_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_tax(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_tax = {
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "taxammount": 0.1,
        "includingVAT": True,
    }

    response = client.post("/tax/", headers=headers, json=new_tax)

    assert response.status_code == 200
    assert response.json()["id"] is not None


def test_add_tax_within_existing_tax_period(client, tax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_tax = {
        "valid_from": tax.valid_from.strftime("%Y-%m-%dT%H:%M:%S"),
        "valid_to": tax.valid_to.strftime("%Y-%m-%dT%H:%M:%S"),
        "taxammount": 0.1,
        "includingVAT": True,
    }

    response = client.post("/tax/", headers=headers, json=new_tax)

    assert response.status_code == 404


def test_add_tax_while_not_logged_in(client, test_session):
    headers = {}

    new_tax = {
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "taxamount": 0.1,
        "includingVAT": True,
    }

    response = client.post("/tax/", headers=headers, json=new_tax)

    assert response.status_code == 401


def test_add_tax_with_missing_data(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_tax = {
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        # Missing taxamount
        "includingVAT": True,
    }

    response = client.post("/tax/", headers=headers, json=new_tax)

    assert response.status_code == 422
