"""
1. Successfully add a new device to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/devices/{device_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_addopt_device(client, user, test_session, chargeowner, deviceNotAdopted):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = deviceNotAdopted.uuid

    data = {
        "uuid": uuid,
        "name": "name",
        "chargeowner_id": chargeowner.id,
        "price_area": "DK2",
        "is_electric_heated": True,
    }

    response = client.post(f"/device/adopt/{uuid}", headers=headers, json=data)

    assert response.status_code == 200
    assert response.json()["uuid"] == uuid
    assert response.json()["name"] == data["name"]
    assert response.json()["chargeowner_id"] == data["chargeowner_id"]
    assert response.json()["price_area"] == data["price_area"]
    assert response.json()["is_electric_heated"] == data["is_electric_heated"]


def test_addopt_device_already_adopted(client, user, test_session, chargeowner, device):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = device.uuid

    data = {
        "uuid": uuid,
        "name": "name",
        "chargeowner_id": chargeowner.id,
        "price_area": "DK2",
        "is_electric_heated": True,
    }

    response = client.post(f"/device/adopt/{uuid}", headers=headers, json=data)

    assert response.status_code == 400


def test_addopt_device_while_not_logged_id(client, test_session, chargeowner, deviceNotAdopted):
    headers = {}

    uuid = deviceNotAdopted.uuid

    data = {
        "uuid": uuid,
        "name": "name",
        "chargeowner_id": chargeowner.id,
        "price_area": "DK2",
        "is_electric_heated": True,
    }

    response = client.post(f"/device/adopt/{uuid}", headers=headers, json=data)

    assert response.status_code == 401


def test_addopt_device_no_chargeowner(client, user, test_session, deviceNotAdopted):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = deviceNotAdopted.uuid

    data = {
        "uuid": uuid,
        "name": "name",
        "chargeowner_id": 100,
        "price_area": "DK2",
        "is_electric_heated": True,
    }

    response = client.post(f"/device/adopt/{uuid}", headers=headers, json=data)

    assert response.status_code == 404


def test_addopt_device_wrong_pricearea(client, user, test_session, chargeowner, deviceNotAdopted):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = deviceNotAdopted.uuid

    data = {
        "uuid": uuid,
        "name": "name",
        "chargeowner_id": chargeowner.id,
        "price_area": "Something_wrong",
        "is_electric_heated": True,
    }

    response = client.post(f"/device/adopt/{uuid}", headers=headers, json=data)

    assert response.status_code == 400
