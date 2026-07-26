def test_signup(client):
    response = client.post(
        "/auth/signup",
        json={"email": "new@example.com", "password": "securepass123"},
    )
    assert response.status_code == 201
    assert response.json()["email"] == "new@example.com"


def test_signup_duplicate_email(client):
    client.post(
        "/auth/signup",
        json={"email": "dupe@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/auth/signup",
        json={"email": "dupe@example.com", "password": "anotherpass123"},
    )
    assert response.status_code == 409


def test_login_success(client):
    client.post(
        "/auth/signup",
        json={"email": "login@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "securepass123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client):
    client.post(
        "/auth/signup",
        json={"email": "wrongpass@example.com", "password": "securepass123"},
    )
    response = client.post(
        "/auth/login",
        data={"username": "wrongpass@example.com", "password": "incorrect"},
    )
    assert response.status_code == 401


def test_me_requires_auth(client):
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_with_auth(client, auth_headers):
    response = client.get("/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"