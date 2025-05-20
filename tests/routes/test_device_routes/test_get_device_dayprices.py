"""
1. Successfully add a new device to the DB
2. if data is missing return 422
3. If the user is not authenticated, return 401
/devices/{device_id}
"""

from datetime import datetime
from zoneinfo import ZoneInfo

from src.fastapi_app.services.user import _generate_tokens


def test_get_device_dayprices_success(
    client, user, device, spotprices_for_all_day, tax, tarif, charge, chargeowner, test_session
):
    data = _generate_tokens(user, test_session)
    headers = {"Authorization": f"Bearer {data['access_token']}"}

    uuid = device.uuid
    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    qdate = datetime.now(copenhagen_tz).strftime("%Y-%m-%d")

    response = client.get("/device/dayprices", headers=headers, params={"qdate": qdate, "uuid": uuid})

    assert response.status_code == 200
    assert response.json()["uuid"] is not None
