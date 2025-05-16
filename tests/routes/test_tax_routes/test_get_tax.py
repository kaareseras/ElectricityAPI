"""
Tests for tax routes.
Functions:
1. Test fetching a tax by ID.
2. Test fetching all taxes.
3. Test fetching today's tax.
4. Test fetching a tax for a specific date.
5. Test fetching a tax for a specific date when no tax is found.
6. Test fetching a tax with an invalid ID.
7. Test fetching a tax without being logged in.
"""

from datetime import datetime, timedelta

from src.fastapi_app.services.user import _generate_tokens

# Test for fetching tax by ID


def test_fetch_tax(client, tax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/tax/id/{tax.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == tax.id


# Test for fetching all taxes


def test_fetch_all_taxes(client, tax, oldtax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/tax", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


# Test for fetching tax for today


def test_fetch_tax_today(client, tax, oldtax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/tax/date", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == tax.id


# Test for fetching tax for a specific date


def test_fetch_tax_specific_date(client, tax, oldtax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now() - timedelta(days=10)

    response = client.get("/tax/date", headers=headers, params={"qdate": qdate})

    print(response.json())

    assert response.status_code == 200
    assert response.json()["id"] == oldtax.id


# Test for fetching tax for a specific date when no tax is found


def test_fetch_tax_specific_date_not_found(client, tax, oldtax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now() - timedelta(days=100)

    response = client.get("/tax/date", headers=headers, params={"qdate": qdate})

    print(response.json())

    assert response.status_code == 404


# Test for fetching tax with an invalid ID


def test_fetch_tax_with_wrong_id(client, tax, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/tax/id/-1", headers=headers)

    assert response.status_code == 404


# Test for fetching tax without being logged in


def test_fetch_tax_while_not_logged_in(client, tax):
    response = client.get(f"/tax/id/{tax.id}")

    assert response.status_code == 401
