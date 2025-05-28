from src.fastapi_app.models.spotprice import Spotprice
from src.fastapi_app.services.user import _generate_tokens


async def test_load_spotprices(client, user, test_session):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}
    test_data = {
        "deliveryDateCET": "2025-05-28",
        "version": 1,
        "updatedAt": "2025-05-27T11:00:00Z",
        "deliveryAreas": ["DK1", "DK2"],
        "market": "DayAhead",
        "multiAreaEntries": [
            {
                "deliveryStart": "2025-05-27T22:00:00Z",
                "deliveryEnd": "2025-05-27T23:00:00Z",
                "entryPerArea": {"DK1": 100.0, "DK2": 200.0},
            },
            {
                "deliveryStart": "2025-05-27T23:00:00Z",
                "deliveryEnd": "2025-05-28T00:00:00Z",
                "entryPerArea": {"DK1": 110.0, "DK2": 210.0},
            },
        ],
    }

    response = client.post("/spotprice/nordpool", headers=headers, json=test_data)
    assert response.status_code == 200
    assert response.json() == {"inserted": 4}

    # Verify entries in the DB
    result = test_session.execute(Spotprice.__table__.select().order_by(Spotprice.HourUTC, Spotprice.PriceArea))
    rows = result.fetchall()
    assert len(rows) == 4


async def test_load_spotprices_not_logged_in(client, test_session):
    headers = {}
    test_data = {
        "deliveryDateCET": "2025-05-28",
        "version": 1,
        "updatedAt": "2025-05-27T11:00:00Z",
        "deliveryAreas": ["DK1", "DK2"],
        "market": "DayAhead",
        "multiAreaEntries": [
            {
                "deliveryStart": "2025-05-27T22:00:00Z",
                "deliveryEnd": "2025-05-27T23:00:00Z",
                "entryPerArea": {"DK1": 100.0, "DK2": 200.0},
            },
            {
                "deliveryStart": "2025-05-27T23:00:00Z",
                "deliveryEnd": "2025-05-28T00:00:00Z",
                "entryPerArea": {"DK1": 110.0, "DK2": 210.0},
            },
        ],
    }

    response = client.post("/spotprice/nordpool", headers=headers, json=test_data)
    assert response.status_code == 401
