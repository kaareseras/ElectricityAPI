import os
import sys
from datetime import datetime, timezone

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.models.device import Device
from src.fastapi_app.models.devicetype import DeviceType


@pytest.fixture(scope="function")
def device(test_session, chargeowner, user, devicetype):
    model = Device()
    model.uuid = "ABC123"
    model.user_id = user.id
    model.name = "Test Device"
    model.chargeowner_id = chargeowner.id
    model.devicetype_id = devicetype.id
    model.price_area = "DK2"
    model.is_electric_heated = False
    model.retail_markup = 0.1
    model.config = '{"setting1": "value1", "setting2": "value2"}'
    model.is_adopted = True
    model.adopted_at = datetime.now(timezone.utc)
    model.is_blocked = False
    model.blocked_at = None
    model.last_activity = datetime.now(timezone.utc)
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def device2(test_session, chargeowner, user, devicetype):
    model = Device()
    model.uuid = "1234567890"
    model.user_id = user.id
    model.name = "Test Device 2"
    model.chargeowner_id = chargeowner.id
    model.devicetype_id = devicetype.id
    model.price_area = "DK2"
    model.is_electric_heated = False
    model.retail_markup = 0.2
    model.config = '{"setting1": "value1", "setting2": "value2"}'
    model.is_adopted = True
    model.adopted_at = datetime.now(timezone.utc)
    model.is_blocked = False
    model.blocked_at = None
    model.last_activity = datetime.now(timezone.utc)
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def deviceNotAdopted(test_session, chargeowner, user, devicetype):
    uuid = "1234567890"
    model = Device()
    model.uuid = uuid
    model.user_id = None
    model.name = uuid
    model.chargeowner_id = None
    model.devicetype_id = devicetype.id
    model.price_area = None
    model.is_electric_heated = False
    model.retail_markup = None
    model.config = None
    model.is_adopted = False
    model.adopted_at = None
    model.is_blocked = False
    model.blocked_at = None
    model.last_activity = datetime.now(timezone.utc)
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def deviceBlocked(test_session, chargeowner, user, devicetype):
    model = Device()
    model.uuid = "1234567890"
    model.user_id = user.id
    model.name = "Test Device 2"
    model.chargeowner_id = chargeowner.id
    model.devicetype_id = devicetype.id
    model.price_area = "DK2"
    model.is_electric_heated = False
    model.retail_markup = 0.1
    model.config = '{"setting1": "value1", "setting2": "value2"}'
    model.is_adopted = True
    model.adopted_at = datetime.now(timezone.utc)
    model.is_blocked = True
    model.blocked_at = datetime.now(timezone.utc)
    model.last_activity = datetime.now(timezone.utc)
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def devicetype(test_session):
    model = DeviceType()
    model.name = "Test Device Type"
    model.hw_version = "1.0"
    model.sw_version = "1.0"
    model.sw_date = datetime.now(timezone.utc).date()
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model
