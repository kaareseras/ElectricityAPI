import os
import sys

import pytest
from starlette.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.email import fm


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
