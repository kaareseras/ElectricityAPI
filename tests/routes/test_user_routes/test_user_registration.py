def test_create_user(client, user_name, user_email, user_password):
    data = {"name": user_name, "email": user_email, "password": user_password}
    response = client.post("/users", json=data)
    assert response.status_code == 201
    assert "password" not in response.json()


def test_create_user_with_existing_email(client, inactive_user, user_password):
    data = {"name": "Keshari Nandan", "email": inactive_user.email, "password": user_password}
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_invalid_email(client, user, user_password):
    data = {"name": "Keshari Nandan", "email": "keshari.com", "password": user_password}
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_empty_password(client, user):
    data = {"name": "Keshari Nandan", "email": user.email, "password": ""}
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_numeric_password(client, user):
    data = {"name": "Keshari Nandan", "email": user.email, "password": "1232382318763"}
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_char_password(client, user):
    data = {"name": "Keshari Nandan", "email": user.email, "password": "asjhgahAdF"}
    response = client.post("/users/", json=data)
    assert response.status_code != 201


def test_create_user_with_alphanumeric_password(client, user):
    data = {"name": "Keshari Nandan", "email": user.email, "password": "sjdgajhGG27862"}
    response = client.post("/users/", json=data)
    assert response.status_code != 201
