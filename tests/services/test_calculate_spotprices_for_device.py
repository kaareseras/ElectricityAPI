from datetime import datetime
from zoneinfo import ZoneInfo

import pytest

from src.fastapi_app.responses.dayprice import hourPrice
from src.fastapi_app.services.device import fetch_device_dayprice  # Import the missing function


@pytest.mark.asyncio
async def test_fetch_device_dayprice_structure(
    client, device, spotprices_for_all_day, tax, tarif, charge, chargeowner, user, test_session
):
    # Arrange
    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    test_date = datetime.now(copenhagen_tz)

    # Act
    result = await fetch_device_dayprice(device.uuid, test_date, test_session)
    prices = result.prices

    # Assert: Should be 24 hourly entries
    assert isinstance(prices, list)
    assert len(prices) == 24
    assert all(isinstance(p, hourPrice) for p in prices)

    # Check isMax / isMin appear only once
    is_max_list = [p.isMax for p in prices]
    is_min_list = [p.isMin for p in prices]

    assert sum(is_max_list) == 1, "Should only have one isMax=True"
    assert sum(is_min_list) == 1, "Should only have one isMin=True"

    # Check they are native bools (not numpy.bool_)
    assert all(type(flag) is bool for flag in is_max_list + is_min_list), "Flags must be of type 'bool'"
