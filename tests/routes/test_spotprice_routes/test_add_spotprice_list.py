"""
1. Succesfull add a new spotprice to the DB
2. If the user is not authenticated, return 401
/chargers/{charger_id}
"""

from src.fastapi_app.services.user import _generate_tokens


def test_add_spotprice_list(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    new_spotprice_list = [
        {
            "HourUTC": "2025-01-04T00:00:00",
            "HourDK": "2025-01-05T00:00:00",
            "PriceArea": "DK2",
            "SpotpriceDKK": 0.4,
        },
        {
            "HourUTC": "2025-01-05T01:00:00",
            "HourDK": "2025-01-06T01:00:00",
            "PriceArea": "DK2",
            "SpotpriceDKK": 0.5,
        },
        {
            "HourUTC": "2025-01-06T02:00:00",
            "HourDK": "2025-01-07T02:00:00",
            "PriceArea": "DK2",
            "SpotpriceDKK": 0.6,
        },
    ]

    response = client.post("/spotprice/bulk/", headers=headers, json=new_spotprice_list)

    assert response.status_code == 200

    response_data = response.json()
    assert len(response_data) == 3


def test_add_spotprice_while_not_logged_in(client, test_session):
    headers = {}

    new_spotprice = [
        {
            "HourUTC": "2025-01-04T00:00:00",
            "HourDK": "2025-01-05T00:00:00",
            "PriceArea": "DK2",
            "SpotpriceDKK": 0.4,
        }
    ]

    response = client.post("/spotprice/", headers=headers, json=new_spotprice)

    assert response.status_code == 401
