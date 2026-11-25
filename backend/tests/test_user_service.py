
import pytest

from app.models.user import User

from app.crud.crud_user import insert_user_in_database

from app.services.user_service import (
    read_user,
    list_users,
    remove_user,
)

from app.exceptions.user_exceptions import (
    UserNotFound,
    UserDeletionConflictError,
)


# ---------- Função auxiliar ----------

def create_test_user(database, email="teste@email.com"):
    user = User(
        name="Usuário Teste",
        email=email,
        password_hash="hash_de_teste",
        role="contractor",
    )

    return insert_user_in_database(
        database=database,
        user=user,
    )


# ---------- READ USER ----------

def test_read_user(database):
    user = create_test_user(database)

    result = read_user(
        database=database,
        user_id=user.id,
    )

    assert result.id == user.id
    assert result.email == user.email
    assert result.name == user.name


def test_read_user_not_found(database):
    with pytest.raises(UserNotFound):
        read_user(
            database=database,
            user_id=999999,
        )


# ---------- LIST USERS ----------

def test_list_users(database):
    first = create_test_user(
        database,
        email="first@email.com",
    )

    second = create_test_user(
        database,
        email="second@email.com",
    )

    results = list_users(database=database)

    assert len(results) == 2
    assert {user.id for user in results} == {first.id, second.id}


def test_list_users_pagination(database):
    first = create_test_user(
        database,
        email="first@email.com",
    )

    second = create_test_user(
        database,
        email="second@email.com",
    )

    third = create_test_user(
        database,
        email="third@email.com",
    )

    results = list_users(
        database=database,
        limit=2,
        offset=0,
    )

    assert len(results) == 2
    assert [user.id for user in results] == [
        first.id,
        second.id,
    ]

    next_results = list_users(
        database=database,
        limit=2,
        offset=2,
    )

    assert [user.id for user in next_results] == [third.id]


def test_list_users_empty(database):
    results = list_users(database=database)

    assert results == []


# ---------- REMOVE USER ----------

def test_remove_user(database):
    user = create_test_user(database)

    result = remove_user(
        database=database,
        user_id=user.id,
    )

    assert result is None


def test_remove_user_not_found(database):
    with pytest.raises(UserNotFound):
        remove_user(
            database=database,
            user_id=999999,
        )


def test_remove_user_with_related_posts(database):
    user = create_test_user(database)

    from app.models.post import Post
    from app.crud.crud_post import insert_post

    post = Post(
        user_id=user.id,
        title="Publicação de teste",
        description="Descrição de teste",
        category="Programação",
    )

    insert_post(database=database, post=post)

    with pytest.raises(UserDeletionConflictError):
        remove_user(
            database=database,
            user_id=user.id,
        )
