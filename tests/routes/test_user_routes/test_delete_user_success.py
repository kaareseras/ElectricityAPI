from src.fastapi_app.models.user import User
from src.fastapi_app.services.user import _generate_tokens


def test_admin_can_delete_user(admin_auth_client, target_user, test_session):
    response = admin_auth_client.delete(f"/users/{target_user.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == target_user.id
    assert test_session.query(User).filter_by(id=target_user.id).first() is None


def test_admin_cannot_delete_own_account(admin_auth_client, admin_user):
    response = admin_auth_client.delete(f"/users/{admin_user.id}")
    assert response.status_code == 400
    assert response.json()["detail"] == "You cannot delete your own account."


def test_non_admin_cannot_delete_user(client, user, target_user, test_session):
    # client uses regular user token
    access_token = _generate_tokens(user, test_session)["access_token"]
    client.headers["Authorization"] = f"Bearer {access_token}"

    response = client.delete(f"/users/{target_user.id}")
    assert response.status_code == 403
    assert response.json()["detail"] == "Admin access required."
