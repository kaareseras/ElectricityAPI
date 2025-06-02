"""
1. Successfully add a new charge to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/chargers/{charger_id}
"""

from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from src.fastapi_app.services.user import _generate_tokens


def test_add_charge(client, chargeowner, user, test_session):
    fake_now = datetime(2025, 1, 4, 0, 0, 0)
    with patch("src.fastapi_app.utils.time_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

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


def test_add_charge_with_default_end_date(client, chargeowner, charge_default_end, user, test_session):
    fake_now = datetime(2025, 1, 4, 0, 0, 0)
    with patch("src.fastapi_app.utils.time_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        data = _generate_tokens(user, test_session)
        headers = {"Authorization": f"Bearer {data['access_token']}"}

        new_charge = {
            "chargeowner_id": chargeowner.id,
            "charge_type": "Type1",
            "charge_type_code": "Code1",
            "note": "Test note",
            "description": "Test description",
            "valid_from": datetime.now(timezone.utc).date().strftime("%Y-%m-%dT%H:%M:%S"),
            "valid_to": (datetime.now(timezone.utc) + timedelta(days=1)).date().strftime("%Y-%m-%dT%H:%M:%S"),
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

        # insert the new record
        response = client.post("/charge/", headers=headers, json=new_charge)
        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)

        # Get the old record
        response = client.get(f"/charge/{charge_default_end.id}", headers=headers)
        assert response.status_code == 200
        assert response.json()["id"] == charge_default_end.id
        assert response.json()["valid_from"] == charge_default_end.valid_from.isoformat()
        assert response.json()["valid_to"] == new_charge["valid_from"]


def test_add_charge_within_existing_charge__with_other_period_but_same_data(
    client, chargeowner, charge_prev, user, test_session
):
    fake_now = datetime(2025, 1, 4, 0, 0, 0)
    with patch("src.fastapi_app.utils.time_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        data = _generate_tokens(user, test_session)
        headers = {"Authorization": f"Bearer {data['access_token']}"}

        new_charge = {
            "chargeowner_id": chargeowner.id,
            "charge_type": charge_prev.charge_type,
            "charge_type_code": charge_prev.charge_type_code,
            "note": charge_prev.note,
            "description": charge_prev.description,
            "valid_from": (charge_prev.valid_to).date().strftime("%Y-%m-%dT%H:%M:%S"),
            "valid_to": (charge_prev.valid_to + timedelta(days=2)).date().strftime("%Y-%m-%dT%H:%M:%S"),
            "price1": charge_prev.price1,
            "price2": charge_prev.price2,
            "price3": charge_prev.price3,
            "price4": charge_prev.price4,
            "price5": charge_prev.price5,
            "price6": charge_prev.price6,
            "price7": charge_prev.price7,
            "price8": charge_prev.price8,
            "price9": charge_prev.price9,
            "price10": charge_prev.price10,
            "price11": charge_prev.price11,
            "price12": charge_prev.price12,
            "price13": charge_prev.price13,
            "price14": charge_prev.price14,
            "price15": charge_prev.price15,
            "price16": charge_prev.price16,
            "price17": charge_prev.price17,
            "price18": charge_prev.price18,
            "price19": charge_prev.price19,
            "price20": charge_prev.price20,
            "price21": charge_prev.price21,
            "price22": charge_prev.price22,
            "price23": charge_prev.price23,
            "price24": charge_prev.price24,
        }

        # insert the new record
        response = client.post("/charge/", headers=headers, json=new_charge)
        assert response.status_code == 200
        assert isinstance(response.json()["id"], int)
        assert response.json()["id"] == charge_prev.id
        assert response.json()["valid_to"] == new_charge["valid_to"]
        assert response.json()["valid_from"] == charge_prev.valid_from.isoformat()


def test_add_charge_within_existing_charge_periode(client, chargeowner, charge, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    fake_now = datetime(2025, 1, 4, 0, 0, 0)
    with patch("src.fastapi_app.utils.time_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

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
    fake_now = datetime(2025, 1, 4, 0, 0, 0)
    with patch("src.fastapi_app.utils.time_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

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
    fake_now = datetime(2025, 1, 4, 0, 0, 0)
    with patch("src.fastapi_app.utils.time_utils.datetime") as mock_datetime:
        mock_datetime.now.return_value = fake_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

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
