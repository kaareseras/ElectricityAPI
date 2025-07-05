import os
import sys

import pytest
import time_machine
from passlib.context import CryptContext

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.fixtures.auth_fixtures import *
from tests.fixtures.charge_chargeowner_fixtures import *
from tests.fixtures.client_fixtures import *
from tests.fixtures.db_fixtures import *
from tests.fixtures.device_devicetype_fixtures import *
from tests.fixtures.spotprice_fixtures import *
from tests.fixtures.tax_tarif_fixtures import *
from tests.fixtures.user_fixtures import *


@pytest.fixture(autouse=True, scope="function")
def freeze_time():
    with time_machine.travel("2025-04-01 00:00 +0000", tick=False):
        yield


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
