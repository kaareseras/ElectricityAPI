"""
1. Successfully add a new tarif to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/tarifs/{tarif_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_tarif(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_tarif = {
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "nettarif": 0.1,
        "systemtarif": 0.2,
        "includingVAT": True,
    }

    response = client.post("/tarif/", headers=headers, json=new_tarif)

    assert response.status_code == 200
    assert response.json()["id"] is not None


def test_add_tarif_within_existing_tarif_period(client, tarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_tarif = {
        "valid_from": tarif.valid_from.strftime("%Y-%m-%dT%H:%M:%S"),
        "valid_to": tarif.valid_to.strftime("%Y-%m-%dT%H:%M:%S"),
        "nettarif": 0.1,
        "systemtarif": 0.2,
        "includingVAT": True,
    }

    response = client.post("/tarif/", headers=headers, json=new_tarif)

    assert response.status_code == 404


def test_add_tarif_while_not_logged_in(client, test_session):
    headers = {}

    new_tarif = {
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        "nettarif": 0.1,
        "systemtarif": 0.2,
        "includingVAT": True,
    }

    response = client.post("/tarif/", headers=headers, json=new_tarif)

    assert response.status_code == 401


def test_add_tarif_with_missing_data(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_tarif = {
        "valid_from": "2025-01-04T00:00:00",
        "valid_to": "2025-01-05T00:00:00",
        # Missing nettarif and systemtarif
        "includingVAT": True,
    }

    response = client.post("/tarif/", headers=headers, json=new_tarif)

    assert response.status_code == 422
