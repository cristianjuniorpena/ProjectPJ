def test_register_user(client):
    payload = {
        "name": "Usuário Teste",
        "email": "register@example.com",
        "password": "senha_segura_123",
        "role": "contractor"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["role"] == payload["role"]
    assert "id" in data
    assert "created_at" in data
    assert "password_hash" not in data
    assert "password" not in data


def test_register_duplicate_email(client):
    payload = {
        "name": "Usuário Teste",
        "email": "duplicate@example.com",
        "password": "senha_segura_123",
        "role": "contractor"
    }

    first_response = client.post("/auth/register", json=payload)
    second_response = client.post("/auth/register", json=payload)

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_register_invalid_email(client):
    payload = {
        "name": "Usuário Teste",
        "email": "email_invalido",
        "password": "senha_segura_123",
        "role": "contractor"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_short_password(client):
    payload = {
        "name": "Usuário Teste",
        "email": "short@example.com",
        "password": "123",
        "role": "contractor"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_register_invalid_role(client):
    payload = {
        "name": "Usuário Teste",
        "email": "role@example.com",
        "password": "senha_segura_123",
        "role": "admin"
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 422


def test_login(client):
    register_payload = {
        "name": "Usuário Teste",
        "email": "login@example.com",
        "password": "senha_segura_123",
        "role": "contractor"
    }

    client.post("/auth/register", json=register_payload)

    response = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "senha_segura_123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_payload = {
        "name": "Usuário Teste",
        "email": "wrongpass@example.com",
        "password": "senha_segura_123",
        "role": "contractor"
    }

    client.post("/auth/register", json=register_payload)

    response = client.post(
        "/auth/login",
        data={
            "username": "wrongpass@example.com",
            "password": "senha_incorreta"
        }
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    response = client.post(
        "/auth/login",
        data={
            "username": "inexistente@example.com",
            "password": "senha_segura_123"
        }
    )

    assert response.status_code == 401


def test_login_token_access_protected_route(client):
    register_payload = {
        "name": "Usuário Teste",
        "email": "protected@example.com",
        "password": "senha_segura_123",
        "role": "contractor"
    }

    client.post("/auth/register", json=register_payload)

    login_response = client.post(
        "/auth/login",
        data={
            "username": "protected@example.com",
            "password": "senha_segura_123"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/user/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "protected@example.com"