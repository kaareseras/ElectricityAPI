import os
import sys
from datetime import UTC, datetime, timedelta, timezone

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.models.charge import Charge
from src.fastapi_app.models.chargeowner import Chargeowner


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
