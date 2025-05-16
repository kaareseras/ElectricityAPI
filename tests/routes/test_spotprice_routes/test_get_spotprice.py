"""
1. Get Charge Owner details
2. If requesting a Charge Owner not in DB return 404
3. If the user is not authenticated, return 401
4. Return spotprices of correct date and pricearea
/chargeowners/{chargeowner_id}
"""

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from src.fastapi_app.services.user import _generate_tokens


def test_fetch_spotprice(client, spotprice, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get(f"/spotprice/{spotprice.id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == spotprice.id


def test_fetch_spotprice_with_wrong_id(client, spotprice, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    response = client.get("/spotprice/-1", headers=headers)

    assert response.status_code == 404


def test_fetch_spotprice_while_not_logged_in(client, spotprice):
    response = client.get(f"/spotprice/{spotprice.id}")

    assert response.status_code == 401


def test_fetch_spotprice_by_date_with_no_date(
    client, spotprice_today, spotprice_yesterday, spotprice_tommorow, user, test_session
):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    response = client.get("/spotprice/date/area", headers=headers, params={"pricearea": "DK2"})

    print(response.json())

    assert response.status_code == 200
    assert len(response.json()) == 1

    assert datetime.fromisoformat(response.json()[0]["HourDK"]).date() == datetime.now().date()


def test_fetch_spotprice_by_date_and_area_for_tommorow(
    client, spotprice_today, spotprice_yesterday, spotprice_tommorow, user, test_session
):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    qdate = (datetime.now(copenhagen_tz) + timedelta(days=1)).date()

    response = client.get("/spotprice/date/area", headers=headers, params={"qdate": qdate, "pricearea": "DK2"})

    print(response.json())

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert (
        datetime.fromisoformat(response.json()[0]["HourDK"]).date()
        == (datetime.now(copenhagen_tz) + timedelta(days=1)).date()
    )
