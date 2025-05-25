"""
Tests for charge routes.
Functions:
1. Test fetching a charge by ID.
2. Test fetching all charges for a charge owner.
3. Test fetching all charges for a non-existent charge owner.
4. Test fetching all charges for a charge owner with no charges.
5. Test fetching a charge with an invalid ID.
6. Test fetching a charge without being logged in.
7. Test fetching a charge by date and charge owner.
8. Test fetching a charge by charge owner.
9. Test fetching a charge by charge owner and date.
10. Test fetching a charge by charge owner and date when no charge owner is found.
11. Test fetching a charge by charge owner and date when no charge is found.
"""

from datetime import UTC, datetime, timedelta

from src.fastapi_app.services.user import _generate_tokens


def test_fetch_charge(client, charge, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/charge/{charge.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == charge.id


def test_fetch_all_charges_for_chargeowner(client, charge, charge_prev, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    chargeowner_gln = chargeowner.glnnumber

    response = client.get(f"/charge/gln/{chargeowner_gln}", headers=headers)

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_fetch_all_charges_for_chargeowner_no_chargeowner(client, charge, charge_prev, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    chargeowner_gln = 1234

    response = client.get(f"/charge/gln/{chargeowner_gln}", headers=headers)

    assert response.status_code == 404


def test_fetch_all_charges_for_chargeowner_no_charges(client, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    chargeowner_gln = chargeowner.glnnumber

    response = client.get(f"/charge/gln/{chargeowner_gln}", headers=headers)

    assert response.status_code == 404


def test_fetch_charge_with_wrong_id(client, charge, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/charge/-1", headers=headers)

    assert response.status_code == 404


def test_fetch_charge_while_not_logged_in(client, charge):
    response = client.get(f"/charge/{charge.id}")

    assert response.status_code == 401


def test_fetch_charge_by_date_and_chargeowner(client, charge, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now().date()
    chargeowner_gln = chargeowner.glnnumber

    response = client.get(
        "/charge/date/gln", headers=headers, params={"qdate": qdate, "chargeowner_glnnumber": chargeowner_gln}
    )

    assert response.status_code == 200
    assert response.json()["id"] == charge.id
    valid_from = datetime.strptime(response.json()["valid_from"], "%Y-%m-%dT%H:%M:%S").date()
    valid_to = datetime.strptime(response.json()["valid_to"], "%Y-%m-%dT%H:%M:%S").date()
    assert valid_from <= qdate < valid_to


def test_fetch_charge_by_chargeowner_gln(client, charge, charge_prev, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    chargeowner_gln = chargeowner.glnnumber

    response = client.get("/charge/date/gln", headers=headers, params={"chargeowner_glnnumber": chargeowner_gln})

    assert response.status_code == 200
    valid_from = datetime.strptime(response.json()["valid_from"], "%Y-%m-%dT%H:%M:%S").date()
    valid_to = datetime.strptime(response.json()["valid_to"], "%Y-%m-%dT%H:%M:%S").date()
    assert valid_from <= datetime.now().date() < valid_to


def test_fetch_charge_by_chargeowner_id(client, charge, charge_prev, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/charge/chargeowner/{chargeowner.id}", headers=headers)
    charges = response.json()
    assert response.status_code == 200
    assert isinstance(charges, list)
    assert len(charges) == 2


def test_fetch_charge_by_chargeowner_and_date(client, charge, charge_prev, chargeowner, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now(UTC).date() - timedelta(days=3)
    chargeowner_gln = chargeowner.glnnumber

    response = client.get(
        "/charge/date/gln", headers=headers, params={"qdate": qdate, "chargeowner_glnnumber": chargeowner_gln}
    )

    assert response.status_code == 200
    valid_from = datetime.strptime(response.json()["valid_from"], "%Y-%m-%dT%H:%M:%S").date()
    valid_to = datetime.strptime(response.json()["valid_to"], "%Y-%m-%dT%H:%M:%S").date()
    assert valid_from <= qdate < valid_to


def test_fetch_charge_by_chargeowner_and_date_non_chargeowner_found(
    client, charge, charge_prev, chargeowner, user, test_session
):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now(UTC).date() - timedelta(days=3)
    chargeowner_gln = "1234"

    response = client.get(
        "/charge/date/gln", headers=headers, params={"qdate": qdate, "chargeowner_glnnumber": chargeowner_gln}
    )

    assert response.status_code == 404


def test_fetch_charge_by_chargeowner_and_date_no_charge_found(
    client, charge, charge_prev, chargeowner, user, test_session
):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    qdate = datetime.now(UTC).date() - timedelta(days=30)
    chargeowner_gln = chargeowner.glnnumber

    response = client.get(
        "/charge/date/gln", headers=headers, params={"qdate": qdate, "chargeowner_glnnumber": chargeowner_gln}
    )

    assert response.status_code == 404
