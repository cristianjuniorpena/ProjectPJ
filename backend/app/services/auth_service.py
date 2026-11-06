from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreateSchema

def normalize_email(email: str) -> str:
    return email.strip().lower()

def email_existing_verification(database: Session, email: str) -> bool:
    existing_user = database.scalar(
        select(User).where(User.email == email)
    )
    return existing_user is not None

def instantiate_user(user_data: UserCreateSchema, email: str) -> User:
    user = User(
        name=user_data.name,
        email=email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
    )
    return user

def register_user_in_database(database: Session, user: User) -> User:
    try:
        database.add(user)
        database.commit()
        database.refresh(user)

    except IntegrityError as error:
        database.rollback()

        constraint_name = getattr(
            getattr(error.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint_name == "uq_users_email":
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            ) from error

        raise

    return user
    

def register_user(database: Session, user_data: UserCreateSchema) -> User:
    email = normalize_email(str(user_data.email))

    if email_existing_verification(database, email):
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = instantiate_user(user_data, email)

    return register_user_in_database(database, user)