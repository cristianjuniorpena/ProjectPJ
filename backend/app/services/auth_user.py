from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.api.dependencies import get_database
from app.schemas.user import UserCreateSchema

def get_users_from_database(database: Session = Depends(get_database)):
    result = database.execute(select(User))
    all_users = result.scalars().all()
    return all_users

def authenticate_user(database: Session, email: str, password: str):
    user = get_user(Session, email)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

