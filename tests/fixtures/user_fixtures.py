import os
import sys
from datetime import UTC, datetime

import pytest
from sqlalchemy.orm import Session

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from src.fastapi_app.config.security import hash_password
from src.fastapi_app.models.user import User

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
