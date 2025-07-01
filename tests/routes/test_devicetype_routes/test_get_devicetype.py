"""
Tests for devicetype routes.
Functions:
1. Test fetching a devicetype by ID.
2. Test fetching all devicetypes.
3. Test fetching today's devicetype (by sw_date).
4. Test fetching a devicetype for a specific date.
5. Test fetching a devicetype for a specific date when none is found.
6. Test fetching a devicetype with an invalid ID.
7. Test fetching a devicetype without being logged in.
"""

from src.fastapi_app.services.user import _generate_tokens

# Test for fetching devicetype by ID


def test_fetch_devicetype(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/devicetype/id/{devicetype.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == devicetype.id


# Test for fetching all devicetypes


def test_fetch_all_devicetypes(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/devicetype", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


# Test for fetching devicetype with an invalid ID


def test_fetch_devicetype_with_wrong_id(client, devicetype, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/devicetype/id/-1", headers=headers)

    assert response.status_code == 404


# Test for fetching devicetype without being logged in


def test_fetch_devicetype_while_not_logged_in(client, devicetype):
    response = client.get(f"/devicetype/id/{devicetype.id}")

    assert response.status_code == 401
