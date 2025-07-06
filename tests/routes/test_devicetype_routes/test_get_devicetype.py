"""
Tests for devicetype routes.

Includes:
1. Test fetching a devicetype by ID (admin and non-admin).
2. Test fetching a devicetype with firmware and hardware data.
3. Test fetching all devicetypes (admin and non-admin).
4. Test fetching a devicetype with an invalid ID.
5. Test fetching a devicetype without being logged in.
"""

from src.fastapi_app.services.user import _generate_tokens

# Test for fetching devicetype by ID


def test_fetch_devicetype(client, devicetype, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/devicetype/id/{devicetype.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == devicetype.id


def test_fetch_devicetype_not_admin(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/devicetype/id/{devicetype.id}", headers=headers)

    assert response.status_code == 403


# Test for fetching devicetype with fw and hw data


def test_fetch_devicetype_with_fw_and_hw(client, devicetype, hardware, firmware, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/devicetype/with_hw_fw", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == devicetype.id
    assert response.json()[0]["fw_version"] == hardware.version
    assert response.json()[0]["fw_date"] == firmware.created_at.isoformat()
    assert response.json()[0]["hw_version"] == hardware.version


# Test for fetching all devicetypes


def test_fetch_all_devicetypes(client, devicetype, admin_user, test_session):
    data = _generate_tokens(admin_user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/devicetype", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_fetch_all_devicetypes_not_admin(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/devicetype", headers=headers)

    assert response.status_code == 403


# Test for fetching devicetype with an invalid ID


def test_fetch_devicetype_with_wrong_id(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/devicetype/id/-1", headers=headers)

    assert response.status_code == 403


# Test for fetching devicetype without being logged in


def test_fetch_devicetype_while_not_logged_in(client, devicetype):
    response = client.get(f"/devicetype/id/{devicetype.id}")

    assert response.status_code == 401
