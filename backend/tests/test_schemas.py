
import pytest
from pydantic import ValidationError

from app.schemas.user import (
    UserCreateSchema,
    UserReadSchema,
    UserSelectSchema,
)


def test_user_create_valid():
    user = UserCreateSchema(
        name="João Silva",
        email="joao@email.com",
        password="SenhaSegura123",
        role="contractor"
    )

    assert user.name == "João Silva"
    assert user.email == "joao@email.com"
    assert user.role == "contractor"


def test_user_create_invalid_role():
    with pytest.raises(ValidationError):
        UserCreateSchema(
            name="João Silva",
            email="joao@email.com",
            password="SenhaSegura123",
            role="administrator"
        )


def test_user_create_invalid_email():
    with pytest.raises(ValidationError):
        UserCreateSchema(
            name="João Silva",
            email="email-invalido",
            password="SenhaSegura123",
            role="contractor"
        )


def test_user_create_short_name():
    with pytest.raises(ValidationError):
        UserCreateSchema(
            name="A",
            email="joao@email.com",
            password="SenhaSegura123",
            role="contractor"
        )


def test_user_create_short_password():
    with pytest.raises(ValidationError):
        UserCreateSchema(
            name="João Silva",
            email="joao@email.com",
            password="1234567",
            role="contractor"
        )


def test_user_create_long_password():
    with pytest.raises(ValidationError):
        UserCreateSchema(
            name="João Silva",
            email="joao@email.com",
            password="A" * 129,
            role="contractor"
        )
