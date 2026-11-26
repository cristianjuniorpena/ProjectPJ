import pytest

from app.models.user import User
from app.crud.crud_user import (select_user_by_email, select_user, insert_user_in_database, delete_user_in_database)
from app.exceptions.user_exceptions import UserAlreadyExistsError


def create_test_user(email="teste@email.com"):
    return User(
        name="Usuário Teste",
        email=email,
        password_hash="hash_de_teste",
        role="contractor"
    )


def test_insert_user(database):
    user = create_test_user()

    inserted_user = insert_user_in_database(
        database=database,
        user=user
    )

    assert inserted_user.id is not None
    assert inserted_user.email == "teste@email.com"


def test_select_user(database):
    user = create_test_user()

    insert_user_in_database(database=database, user=user)

    result = select_user(
        database=database,
        user_id=user.id
    )

    assert result is not None
    assert result.id == user.id
    assert result.email == user.email


def test_select_user_not_found(database):
    result = select_user(
        database=database,
        user_id=999999
    )

    assert result is None


def test_select_user_by_email(database):
    user = create_test_user()

    insert_user_in_database(database=database, user=user)

    result = select_user_by_email(
        database=database,
        user_email="teste@email.com"
    )

    assert result is not None
    assert result.id == user.id


def test_insert_duplicate_email(database):
    user1 = create_test_user()
    user2 = create_test_user()

    insert_user_in_database(database=database, user=user1)

    with pytest.raises(UserAlreadyExistsError):
        insert_user_in_database(database=database, user=user2)


def test_delete_user(database):
    user = create_test_user()

    insert_user_in_database(database=database, user=user)

    result = delete_user_in_database(
        database=database,
        user_id=user.id
    )

    assert result is True
    assert select_user(database=database, user_id=user.id) is None


def test_delete_user_not_found(database):
    result = delete_user_in_database(
        database=database,
        user_id=999999
    )

    assert result is False
