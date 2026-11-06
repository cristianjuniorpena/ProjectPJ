from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def register_user(database: Session, user_data: UserCreate) -> User:

    email = str(user_data.email).strip().lower()

    existing_user = database.scalar(
        select(User).where(User.email == email)
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = User(
        name=user_data.name,
        email=email,
        password_hash=hash_password(user_data.password),
        role=user_data.role,
    )

    try:
        database.add(user)
        database.commit()
        database.refresh(user)

    except IntegrityError:
        database.rollback()

        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    return user