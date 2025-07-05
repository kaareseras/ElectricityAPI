import os
import sys
from datetime import UTC, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest
import time_machine

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.models.spotprice import Spotprice


@pytest.fixture(scope="function")
def spotprice(test_session):
    model = Spotprice()
    model.HourUTC = datetime(2025, 1, 4, 0, 0, 0, tzinfo=timezone.utc)
    model.HourDK = datetime(2025, 1, 4, 0, 0, 0, tzinfo=timezone.utc)
    model.DateDK = datetime(2025, 1, 4, 0, 0, 0, tzinfo=timezone.utc).date()
    model.PriceArea = "DK2"
    model.SpotpriceDKK = 0.4
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def spotprice_yesterday(test_session):
    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    HourDK = datetime.now(copenhagen_tz).replace(hour=12, minute=0, second=0, microsecond=0)
    HourUTC = HourDK.astimezone(timezone.utc)

    model = Spotprice()
    model.HourUTC = HourUTC - timedelta(days=1)
    model.HourDK = HourDK - timedelta(days=1)
    model.DateDK = HourDK.date() - timedelta(days=1)
    model.PriceArea = "DK2"
    model.SpotpriceDKK = 0.4
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)

    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def spotprice_today(test_session):
    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    HourDK = datetime.now(copenhagen_tz).replace(hour=12, minute=0, second=0, microsecond=0)
    HourUTC = HourDK.astimezone(UTC)

    model = Spotprice()
    model.HourUTC = HourUTC
    model.HourDK = HourDK
    model.DateDK = HourDK.date()
    model.PriceArea = "DK2"
    model.SpotpriceDKK = 0.5
    model.created_at = datetime.now(UTC)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)

    print(f"Spotprice today: {model.DateDK}")
    return model


@time_machine.travel("2025-04-01 00:00 +0000")
@pytest.fixture(scope="function")
def spotprice_tommorow(test_session):
    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    HourDK = datetime.now(copenhagen_tz).replace(hour=12, minute=0, second=0, microsecond=0)
    HourUTC = HourDK.astimezone(timezone.utc)
    model = Spotprice()
    model.HourUTC = HourUTC + timedelta(days=1)
    model.HourDK = HourDK + timedelta(days=1)
    model.DateDK = HourDK.date() + timedelta(days=1)
    model.PriceArea = "DK2"
    model.SpotpriceDKK = 0.6
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)

    test_session.commit()
    test_session.refresh(model)
    return model


@time_machine.travel("2025-04-01 00:00 +0000")
@pytest.fixture(scope="function")
def spotprices_for_all_day(test_session):
    copenhagen_tz = ZoneInfo("Europe/Copenhagen")
    HourDK = datetime.now(copenhagen_tz).replace(hour=0, minute=0, second=0, microsecond=0)
    HourUTC = HourDK.astimezone(UTC)

    spotprices = []
    for hour in range(24):
        model = Spotprice()
        model.HourUTC = HourUTC + timedelta(hours=hour)
        model.HourDK = HourDK + timedelta(hours=hour)
        model.DateDK = HourDK.date()
        model.PriceArea = "DK2"
        model.SpotpriceDKK = 0.5 + hour * 0.01  # Example price variation
        model.created_at = datetime.now(timezone.utc)
        test_session.add(model)
        test_session.commit()
        test_session.refresh(model)
        spotprices.append(model)

    return spotprices
