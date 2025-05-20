"""
Tests for tarif routes.
Functions:
1. Test fetching a tarif by ID.
2. Test fetching all tarifs.
3. Test fetching today's tarif.
4. Test fetching a tarif for a specific date.
5. Test fetching a tarif for a specific date when no tarif is found.
6. Test fetching a tarif with an invalid ID.
7. Test fetching a tarif without being logged in.
"""

from datetime import datetime, timedelta

from src.fastapi_app.services.user import _generate_tokens

# Test for fetching tarif by ID


def test_fetch_tarif(client, tarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/tarif/id/{tarif.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == tarif.id


# Test for fetching all tarifs


def test_fetch_all_tarifs(client, tarif, oldtarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/tarif", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


# Test for fetching tarif for today


def test_fetch_tarif_today(client, tarif, oldtarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/tarif/date", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == tarif.id


# Test for fetching tarif for a specific date


def test_fetch_tarif_specific_date(client, tarif, oldtarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now().date() - timedelta(days=10)

    response = client.get("/tarif/date", headers=headers, params={"qdate": qdate})

    print(response.json())

    assert response.status_code == 200
    assert response.json()["id"] == oldtarif.id


# Test for fetching tarif for a specific date when no tarif is found


def test_fetch_tarif_specific_date_not_found(client, tarif, oldtarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now().date() - timedelta(days=100)

    response = client.get("/tarif/date", headers=headers, params={"qdate": qdate})

    print(response.json())

    assert response.status_code == 404


# Test for fetching tarif with an invalid ID


def test_fetch_tarif_with_wrong_id(client, tarif, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/tarif/id/-1", headers=headers)

    assert response.status_code == 404


# Test for fetching tarif without being logged in


def test_fetch_tarif_while_not_logged_in(client, tarif):
    response = client.get(f"/tarif/id/{tarif.id}")

    assert response.status_code == 401
