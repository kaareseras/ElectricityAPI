import os
import sys
from datetime import datetime, timedelta, timezone

import pytest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.models.tarif import Tarif
from src.fastapi_app.models.tax import Tax


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
