import os
import sys

import pytest
from starlette.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.fastapi_app.config.database import get_db_session
from src.fastapi_app.config.email import fm
from src.fastapi_app.services.user import _generate_tokens


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


@pytest.fixture
def admin_auth_client(app_test, test_session, admin_user):
    def _override_db():
        yield test_session

    app_test.dependency_overrides[get_db_session] = _override_db
    access_token = _generate_tokens(admin_user, test_session)["access_token"]

    client = TestClient(app_test)
    client.headers["Authorization"] = f"Bearer {access_token}"
    return client
