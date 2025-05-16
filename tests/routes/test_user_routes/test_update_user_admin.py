from fastapi import status


def test_admin_can_update_other_user_to_admin(client, admin_auth_client, normal_user, test_session):
    response = admin_auth_client.put(f"/users/admin/{normal_user.id}/true")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == normal_user.id
    assert data["is_admin"] is True


def test_admin_cannot_update_self(client, admin_auth_client, admin_user, test_session):
    response = admin_auth_client.put(f"/users/admin/{admin_user.id}/false")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "You cannot update your own account."


def test_admin_update_nonexistent_user(client, admin_auth_client, test_session):
    response = admin_auth_client.put("/users/admin/9999/true")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found."


def test_non_admin_cannot_update_other_user(client, auth_client, normal_user, test_session):
    response = auth_client.put(f"/users/admin/{normal_user.id}/true")
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json()["detail"] == "Admin access required."
