import os
import sys
from collections.abc import Generator
from datetime import UTC, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import pytest
import time_machine
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.fastapi_app.app import app
from src.fastapi_app.config.database import Base, get_db_session
from src.fastapi_app.config.email import fm
from src.fastapi_app.config.security import hash_password
from src.fastapi_app.models.charge import Charge
from src.fastapi_app.models.chargeowner import Chargeowner
from src.fastapi_app.models.device import Device
from src.fastapi_app.models.devicetype import DeviceType
from src.fastapi_app.models.spotprice import Spotprice
from src.fastapi_app.models.tarif import Tarif
from src.fastapi_app.models.tax import Tax
from src.fastapi_app.models.user import User
from src.fastapi_app.services.user import _generate_tokens


@pytest.fixture(autouse=True, scope="function")
def freeze_time():
    with time_machine.travel("2025-04-01 00:00 +0000", tick=False):
        yield


USER_NAME = "kaare"
USER_EMAIL = "kaare@seras.dk"
USER_PASSWORD = "Password3!"


@pytest.fixture
def user_name():
    return USER_NAME


@pytest.fixture
def user_email():
    return USER_EMAIL


@pytest.fixture
def user_password():
    return USER_PASSWORD


engine = create_engine("sqlite:///./fastapi.db")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.fixture(scope="function")
def test_session() -> Generator:
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def app_test():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(app_test, test_session):
    def _test_db():
        try:
            yield test_session
        finally:
            pass

    app_test.dependency_overrides[get_db_session] = _test_db
    fm.config.SUPPRESS_SEND = 1
    return TestClient(app_test)


@pytest.fixture(scope="function")
def auth_client(app_test, test_session, user):
    def _test_db():
        try:
            yield test_session
        finally:
            pass

    app_test.dependency_overrides[get_db_session] = _test_db
    fm.config.SUPPRESS_SEND = 1
    data = _generate_tokens(user, test_session)
    client = TestClient(app_test)
    client.headers["Authorization"] = f"Bearer {data['access_token']}"
    return client


@pytest.fixture(scope="function")
def inactive_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.now(UTC)
    model.is_active = False
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.now(UTC)
    model.verified_at = datetime.now(UTC)
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def unverified_user(test_session):
    model = User()
    model.name = USER_NAME
    model.email = USER_EMAIL
    model.password = hash_password(USER_PASSWORD)
    model.updated_at = datetime.now(UTC)
    model.is_active = True
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture
def admin_user(test_session: Session):
    user = User(
        name="admin",
        email="admin@example.com",
        password=hash_password("AdminPass1!"),
        is_active=True,
        is_admin=True,
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def target_user(test_session: Session):
    user = User(
        name="target",
        email="target@example.com",
        password=hash_password("TargetPass1!"),
        is_active=True,
        is_admin=False,
    )
    test_session.add(user)
    test_session.commit()
    test_session.refresh(user)
    return user


@pytest.fixture
def normal_user(test_session):
    user = User(
        name="normal",
        email="normal@example.com",
        password=hash_password("userpass"),
        is_admin=False,
    )
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def admin_auth_client(app_test, test_session, admin_user):
    def _override_db():
        yield test_session

    app_test.dependency_overrides[get_db_session] = _override_db
    access_token = _generate_tokens(admin_user, test_session)["access_token"]

    client = TestClient(app_test)
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client


@pytest.fixture(scope="function")
def chargeowner(test_session):
    model = Chargeowner()
    model.glnnumber = "5790000705689"
    model.compagny = "Radius Elnet A/S"
    model.chargetype = "D03"
    model.chargetypecode = "DT_C_01"
    model.is_active = True
    model.created_at = datetime.now(UTC)
    model.updated_at = datetime.now(UTC)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


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


@pytest.fixture(scope="function")
def charge(test_session, chargeowner):
    model = Charge()
    model.chargeowner_id = chargeowner.id
    model.charge_type = "Type1"
    model.charge_type_code = "Code1"
    model.note = "Sample note"
    model.description = "Sample description"
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=1)
    model.valid_to = datetime.now(timezone.utc).date() + timedelta(days=1)
    model.price1 = 0.1
    model.price2 = 0.2
    model.price3 = 0.3
    model.price4 = 0.4
    model.price5 = 0.5
    model.price6 = 0.6
    model.price7 = 0.7
    model.price8 = 0.8
    model.price9 = 0.9
    model.price10 = 1.0
    model.price11 = 1.1
    model.price12 = 1.2
    model.price13 = 1.3
    model.price14 = 1.4
    model.price15 = 1.5
    model.price16 = 1.6
    model.price17 = 1.7
    model.price18 = 1.8
    model.price19 = 1.9
    model.price20 = 2.0
    model.price21 = 2.1
    model.price22 = 2.2
    model.price23 = 2.3
    model.price24 = 2.4
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def charge2(test_session, chargeowner):
    model = Charge()
    model.chargeowner_id = chargeowner.id
    model.charge_type = "Type1"
    model.charge_type_code = "Code1"
    model.note = "Another note"
    model.description = "Another description"
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=1)
    model.valid_to = datetime.now(timezone.utc).date() + timedelta(days=1)
    model.price1 = 0.2
    model.price2 = 0.4
    model.price3 = 0.6
    model.price4 = 0.8
    model.price5 = 1.0
    model.price6 = 1.2
    model.price7 = 1.4
    model.price8 = 1.6
    model.price9 = 1.8
    model.price10 = 2.0
    model.price11 = 2.2
    model.price12 = 2.4
    model.price13 = 2.6
    model.price14 = 2.8
    model.price15 = 3.0
    model.price16 = 3.2
    model.price17 = 3.4
    model.price18 = 3.6
    model.price19 = 3.8
    model.price20 = 4.0
    model.price21 = 4.2
    model.price22 = 4.4
    model.price23 = 4.6
    model.price24 = 4.8
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def charge_default_end(test_session, chargeowner):
    model = Charge()
    model.chargeowner_id = chargeowner.id
    model.charge_type = "Type1"
    model.charge_type_code = "Code1"
    model.note = "Sample note"
    model.description = "Sample description"
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=1)
    model.valid_to = datetime(9999, 12, 31, 23, 59, 59)
    model.price1 = 0.1
    model.price2 = 0.2
    model.price3 = 0.3
    model.price4 = 0.4
    model.price5 = 0.5
    model.price6 = 0.6
    model.price7 = 0.7
    model.price8 = 0.8
    model.price9 = 0.9
    model.price10 = 1.0
    model.price11 = 1.1
    model.price12 = 1.2
    model.price13 = 1.3
    model.price14 = 1.4
    model.price15 = 1.5
    model.price16 = 1.6
    model.price17 = 1.7
    model.price18 = 1.8
    model.price19 = 1.9
    model.price20 = 2.0
    model.price21 = 2.1
    model.price22 = 2.2
    model.price23 = 2.3
    model.price24 = 2.4
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def charge_prev(test_session, chargeowner):
    model = Charge()
    model.chargeowner_id = chargeowner.id
    model.charge_type = "Type1"
    model.charge_type_code = "Code1"
    model.note = "Sample note"
    model.description = "Sample description charge_prev"
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=4)
    model.valid_to = datetime.now(timezone.utc).date() - timedelta(days=2)
    model.price1 = 0.1
    model.price2 = 0.2
    model.price3 = 0.3
    model.price4 = 0.4
    model.price5 = 0.5
    model.price6 = 0.6
    model.price7 = 0.7
    model.price8 = 0.8
    model.price9 = 0.9
    model.price10 = 1.0
    model.price11 = 1.1
    model.price12 = 1.2
    model.price13 = 1.3
    model.price14 = 1.4
    model.price15 = 1.5
    model.price16 = 1.6
    model.price17 = 1.7
    model.price18 = 1.8
    model.price19 = 1.9
    model.price20 = 2.0
    model.price21 = 2.1
    model.price22 = 2.2
    model.price23 = 2.3
    model.price24 = 2.4
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def tax(test_session):
    model = Tax()
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=2)
    model.valid_to = datetime.now(timezone.utc).date() + timedelta(days=20)
    model.taxammount = 1.1
    model.includingVAT = False
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def oldtax(test_session):
    model = Tax()
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=12)
    model.valid_to = datetime.now(timezone.utc).date() - timedelta(days=8)
    model.taxammount = 2.1
    model.includingVAT = True
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def tarif(test_session):
    model = Tarif()
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=8)
    model.valid_to = datetime.now(timezone.utc).date() + timedelta(days=22)
    model.nettarif = 1.1
    model.systemtarif = 2.1
    model.includingVAT = True
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


@pytest.fixture(scope="function")
def oldtarif(test_session):
    model = Tarif()
    model.valid_from = datetime.now(timezone.utc).date() - timedelta(days=12)
    model.valid_to = datetime.now(timezone.utc).date() - timedelta(days=8)
    model.nettarif = 1.1
    model.systemtarif = 2.1
    model.includingVAT = True
    model.created_at = datetime.now(timezone.utc)
    test_session.add(model)
    test_session.commit()
    test_session.refresh(model)
    return model


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
