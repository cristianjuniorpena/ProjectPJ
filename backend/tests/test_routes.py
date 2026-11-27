
import jwt
import pytest

from app.core.config import settings
from app.models.user import User
from app.models.post import Post
from app.crud.crud_user import insert_user_in_database
from app.crud.crud_post import insert_post


# ---------- Helpers ----------

def create_test_user(database, email, role="contractor"):
    user = User(
        name="Usuário Teste",
        email=email,
        password_hash="hash_de_teste",
        role=role,
    )

    return insert_user_in_database(database, user)


def create_token(user):
    payload = {
        "sub": str(user.id),
        "email": user.email,
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def auth_headers(user):
    token = create_token(user)
    return {"Authorization": f"Bearer {token}"}


def create_test_post(database, user_id):
    post = Post(
        user_id=user_id,
        title="Desenvolvimento de API",
        description="Preciso de uma API para um projeto.",
        category="Programação",
    )

    return insert_post(database, post)


# ---------- USER ROUTES ----------

def test_get_all_users(client, database):
    first = create_test_user(database, "first@email.com")
    second = create_test_user(database, "second@email.com")

    response = client.get("/user/")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert len(response.json()["users"]) == 2


def test_read_user_me(client, database):
    user = create_test_user(database, "user@email.com")

    response = client.get(
        "/user/me",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert response.json()["id"] == user.id
    assert response.json()["email"] == user.email
    assert "password_hash" not in response.json()


def test_read_user_me_without_token(client):
    response = client.get("/user/me")

    assert response.status_code == 401


def test_read_user_me_invalid_token(client):
    response = client.get(
        "/user/me",
        headers={"Authorization": "Bearer token_invalido"},
    )

    assert response.status_code == 401


def test_read_user_me_deleted_user(client, database):
    user = create_test_user(database, "deleted@email.com")

    token = create_token(user)

    # Exclui o usuário diretamente do banco.
    from app.crud.crud_user import delete_user_in_database
    delete_user_in_database(database, user.id)

    response = client.get(
        "/user/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401


def test_delete_user(client, database):
    user = create_test_user(database, "delete@email.com")

    response = client.delete(
        "/user/delete",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert response.json()["status"] == "sucesso"


def test_delete_user_without_token(client):
    response = client.delete("/user/delete")

    assert response.status_code == 401


def test_delete_user_with_posts(client, database):
    user = create_test_user(database, "owner@email.com")
    create_test_post(database, user.id)

    response = client.delete(
        "/user/delete",
        headers=auth_headers(user),
    )

    assert response.status_code == 400


# ---------- POST ROUTES ----------

def test_get_all_posts(client, database):
    user = create_test_user(database, "owner@email.com")
    create_test_post(database, user.id)

    token = create_token(user)

    response = client.get(
        "/posts/",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


def test_get_post(client, database):
    user = create_test_user(database, "owner@email.com")
    post = create_test_post(database, user.id)

    response = client.get(f"/posts/{post.id}")

    assert response.status_code == 200
    assert response.json()["id"] == post.id


def test_get_post_not_found(client):
    response = client.get("/posts/999999")

    assert response.status_code == 404


def test_get_my_posts(client, database):
    user = create_test_user(database, "owner@email.com")
    post = create_test_post(database, user.id)

    response = client.get(
        "/posts/my-posts",
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == post.id


def test_get_my_posts_provider(client, database):
    provider = create_test_user(
        database,
        "provider@email.com",
        role="provider",
    )

    response = client.get(
        "/posts/my-posts",
        headers=auth_headers(provider),
    )

    assert response.status_code == 403


def test_get_my_posts_without_token(client):
    response = client.get("/posts/my-posts")

    assert response.status_code == 401


def test_create_post(client, database):
    user = create_test_user(database, "owner@email.com")

    payload = {
        "title": "Desenvolvimento de API",
        "description": "Preciso de uma API para um projeto.",
        "category": "Programação",
        "budget": 500.00,
    }

    response = client.post(
        "/posts/",
        json=payload,
        headers=auth_headers(user),
    )

    assert response.status_code == 201
    assert response.json()["title"] == payload["title"]
    assert response.json()["user_id"] == user.id


def test_create_post_provider(client, database):
    provider = create_test_user(
        database,
        "provider@email.com",
        role="provider",
    )

    payload = {
        "title": "Desenvolvimento de API",
        "description": "Preciso de uma API.",
        "category": "Programação",
    }

    response = client.post(
        "/posts/",
        json=payload,
        headers=auth_headers(provider),
    )

    assert response.status_code == 403


def test_create_post_without_token(client):
    payload = {
        "title": "Desenvolvimento de API",
        "description": "Preciso de uma API.",
        "category": "Programação",
    }

    response = client.post("/posts/", json=payload)

    assert response.status_code == 401


def test_create_post_invalid_payload(client, database):
    user = create_test_user(database, "owner@email.com")

    response = client.post(
        "/posts/",
        json={"title": "Título"},
        headers=auth_headers(user),
    )

    assert response.status_code == 422


def test_edit_post(client, database):
    user = create_test_user(database, "owner@email.com")
    post = create_test_post(database, user.id)

    response = client.patch(
        f"/posts/{post.id}",
        json={"title": "Título atualizado"},
        headers=auth_headers(user),
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Título atualizado"


def test_edit_post_another_user(client, database):
    owner = create_test_user(database, "owner@email.com")
    another_user = create_test_user(database, "another@email.com")

    post = create_test_post(database, owner.id)

    response = client.patch(
        f"/posts/{post.id}",
        json={"title": "Tentativa de alteração"},
        headers=auth_headers(another_user),
    )

    assert response.status_code == 403


def test_edit_post_not_found(client, database):
    user = create_test_user(database, "owner@email.com")

    response = client.patch(
        "/posts/999999",
        json={"title": "Novo título"},
        headers=auth_headers(user),
    )

    assert response.status_code == 404


def test_delete_post(client, database):
    user = create_test_user(database, "owner@email.com")
    post = create_test_post(database, user.id)

    response = client.delete(
        f"/posts/{post.id}",
        headers=auth_headers(user),
    )

    assert response.status_code == 204
    assert response.content == b""


def test_delete_post_another_user(client, database):
    owner = create_test_user(database, "owner@email.com")
    another_user = create_test_user(database, "another@email.com")

    post = create_test_post(database, owner.id)

    response = client.delete(
        f"/posts/{post.id}",
        headers=auth_headers(another_user),
    )

    assert response.status_code == 403


def test_delete_post_not_found(client, database):
    user = create_test_user(database, "owner@email.com")

    response = client.delete(
        "/posts/999999",
        headers=auth_headers(user),
    )

    assert response.status_code == 404
