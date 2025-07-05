import os
import sys
from datetime import datetime, timezone

import pytest

from src.fastapi_app.models.firmware import Firmware
from src.fastapi_app.models.hardware import Hardware

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.models.device import Device
from src.fastapi_app.models.devicetype import DeviceType


@pytest.fixture(scope="function")
def device(test_session, chargeowner, user, devicetype, hardware, firmware):
    model = Device()
    model.uuid = "ABC123"
    model.user_id = user.id
    model.name = "Test Device"
    model.chargeowner_id = chargeowner.id
    model.devicetype_id = devicetype.id
    model.firmware_id = firmware.id
    model.hardware_id = hardware.id
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
def device2(test_session, chargeowner, user, devicetype, hardware, firmware):
    model = Device()
    model.uuid = "1234567890"
    model.user_id = user.id
    model.name = "Test Device 2"
    model.chargeowner_id = chargeowner.id
    model.devicetype_id = devicetype.id
    model.firmware_id = firmware.id
    model.hardware_id = hardware.id
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
def deviceNotAdopted(test_session, chargeowner, user, devicetype, hardware, firmware):
    uuid = "1234567890"
    model = Device()
    model.uuid = uuid
    model.user_id = None
    model.name = uuid
    model.chargeowner_id = None
    model.firmware_id = firmware.id
    model.hardware_id = hardware.id
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
def deviceBlocked(test_session, chargeowner, user, devicetype, hardware, firmware):
    model = Device()
    model.uuid = "1234567890"
    model.user_id = user.id
    model.name = "Test Device 2"
    model.chargeowner_id = chargeowner.id
    model.devicetype_id = devicetype.id
    model.firmware_id = firmware.id
    model.hardware_id = hardware.id
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
    model.description = "A description of the test device type."
    model.created_at = datetime.now(timezone.utc).date()
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def hardware(test_session, devicetype):
    model = Hardware()
    model.devicetype_id = devicetype.id
    model.name = "Test Hardware"
    model.version = "1.0"
    model.description = "A description of the test hardware."
    model.created_at = datetime.now(timezone.utc).date()
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def firmware(test_session, devicetype):
    model = Firmware()
    model.devicetype_id = devicetype.id
    model.version = "1.0"
    model.filename = "test_firmware.bin"
    model.repo_url = "http://example.com/test_firmware"
    model.created_at = datetime.now(timezone.utc).date()
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model
