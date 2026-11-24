
from decimal import Decimal

import pytest

from app.models.post import Post
from app.models.user import User

from app.crud.crud_user import insert_user_in_database
from app.crud.crud_post import (
    select_all_posts,
    select_user_posts,
    select_post,
    insert_post,
    verify_invalid_fields,
    update_post,
    delete_post,
)


# ---------- Funções auxiliares ----------

def create_test_user(database):
    user = User(
        name="Contratante Teste",
        email="contratante@email.com",
        password_hash="hash_de_teste",
        role="contractor",
    )

    return insert_user_in_database(database=database, user=user)


def create_test_post(user_id, **overrides):
    data = {
        "user_id": user_id,
        "title": "Desenvolvimento de API",
        "description": "Preciso de uma API para um pequeno projeto.",
        "category": "Programação",
    }

    data.update(overrides)

    return Post(**data)


# ---------- INSERT ----------

def test_insert_post(database):
    user = create_test_user(database)
    post = create_test_post(user.id)

    result = insert_post(database=database, post=post)

    assert result.id is not None
    assert result.user_id == user.id
    assert result.title == "Desenvolvimento de API"
    assert result.budget is None
    assert result.status == "open"


# ---------- SELECT ----------

def test_select_post(database):
    user = create_test_user(database)
    post = insert_post(
        database=database,
        post=create_test_post(user.id),
    )

    result = select_post(database=database, post_id=post.id)

    assert result is not None
    assert result.id == post.id
    assert result.title == post.title


def test_select_post_not_found(database):
    result = select_post(database=database, post_id=999999)

    assert result is None


def test_select_post_invalid_id(database):
    result = select_post(database=database, post_id=0)

    assert result is None


def test_select_user_posts(database):
    user = create_test_user(database)

    first = insert_post(
        database=database,
        post=create_test_post(user.id, title="Primeiro"),
    )

    second = insert_post(
        database=database,
        post=create_test_post(user.id, title="Segundo"),
    )

    results = select_user_posts(database=database, user_id=user.id)

    assert len(results) == 2
    assert {post.id for post in results} == {first.id, second.id}


def test_select_user_posts_empty(database):
    user = create_test_user(database)

    results = select_user_posts(database=database, user_id=user.id)

    assert results == []


# ---------- SELECT ALL / PAGINATION ----------

def test_select_all_posts_pagination(database):
    user = create_test_user(database)

    first = insert_post(
        database=database,
        post=create_test_post(user.id, title="Primeiro"),
    )

    second = insert_post(
        database=database,
        post=create_test_post(user.id, title="Segundo"),
    )

    third = insert_post(
        database=database,
        post=create_test_post(user.id, title="Terceiro"),
    )

    results = select_all_posts(database=database, limit=2, offset=0)

    assert len(results) == 2
    assert [post.id for post in results] == [third.id, second.id]

    next_results = select_all_posts(
        database=database,
        limit=2,
        offset=2,
    )

    assert [post.id for post in next_results] == [first.id]


@pytest.mark.parametrize("limit", [0, -1, 101])
def test_select_all_posts_invalid_limit(database, limit):
    with pytest.raises(ValueError):
        select_all_posts(database=database, limit=limit)


@pytest.mark.parametrize("offset", [-1, -10])
def test_select_all_posts_invalid_offset(database, offset):
    with pytest.raises(ValueError):
        select_all_posts(database=database, offset=offset)


# ---------- FIELD VALIDATION ----------

def test_verify_invalid_fields():
    assert verify_invalid_fields({"title": "Novo título"}) is False
    assert verify_invalid_fields({"user_id": 123}) is True
    assert verify_invalid_fields({}) is False


# ---------- UPDATE ----------

def test_update_post(database):
    user = create_test_user(database)

    post = insert_post(
        database=database,
        post=create_test_post(user.id),
    )

    result = update_post(
        database=database,
        post_id=post.id,
        update_data={
            "title": "Título atualizado",
            "status": "closed",
            "budget": Decimal("500.00"),
        },
    )

    assert result is not None
    assert result.title == "Título atualizado"
    assert result.status == "closed"
    assert result.budget == Decimal("500.00")


def test_update_post_not_found(database):
    result = update_post(
        database=database,
        post_id=999999,
        update_data={"title": "Novo título"},
    )

    assert result is None


def test_update_post_invalid_fields(database):
    user = create_test_user(database)

    post = insert_post(
        database=database,
        post=create_test_post(user.id),
    )

    with pytest.raises(ValueError):
        update_post(
            database=database,
            post_id=post.id,
            update_data={"user_id": 999},
        )


def test_update_post_empty_data(database):
    user = create_test_user(database)

    post = insert_post(
        database=database,
        post=create_test_post(user.id),
    )

    result = update_post(
        database=database,
        post_id=post.id,
        update_data={},
    )

    assert result is not None
    assert result.id == post.id
    assert result.title == post.title


# ---------- DELETE ----------

def test_delete_post(database):
    user = create_test_user(database)

    post = insert_post(
        database=database,
        post=create_test_post(user.id),
    )

    result = delete_post(database=database, post_id=post.id)

    assert result is True
    assert select_post(database=database, post_id=post.id) is None


def test_delete_post_not_found(database):
    result = delete_post(database=database, post_id=999999)

    assert result is False
