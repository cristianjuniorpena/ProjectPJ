from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.crud.crud_user import get_id_by_email, get_user, insert_user_in_database
from app.core.security import hash_password, verify_password_hash
from app.models.user import User
from app.schemas.user import UserCreateSchema
from app.core.config import settings

def normalize_email(email: str) -> str:
    return email.strip().lower()

def email_existing_verification(database: Session, email: str) -> bool:
    existing_user = database.scalar(
        select(User).where(User.email == email)
    )
    return existing_user is not None

def instantiate_user(user_data: UserCreateSchema, email: str) -> User:
    user = User(user_data.name, email, hash_password(user_data.password), user_data.role)
    return user

def register_user(database: Session, user_data: UserCreateSchema) -> User:
    email = normalize_email(str(user_data.email))

    if email_existing_verification(database, email):
        raise HTTPException(
            status_code=409,
            detail="Email already registered",
        )

    user = instantiate_user(user_data, email)

    return insert_user_in_database(database, user)

def authenticate_user(database: Session, email: str, password: str):
    user_id = get_id_by_email(database, email)
    user = get_user(database, user_id)
    if not user:
        verify_password_hash(password, settings.DUMMY_HASH)
        return False
    if not verify_password_hash(password, user.password_hash):
        return False
    return user