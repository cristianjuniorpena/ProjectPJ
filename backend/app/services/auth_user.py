from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import verify_password_hash
from app.core.config import settings

def get_users_from_database(database: Session):
    result = database.execute(select(User))
    all_users = result.scalars().all()
    return all_users

def get_user(database: Session, email: str):
    result = database.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    return user

def authenticate_user(database: Session, email: str, password: str):
    user = get_user(database, email)
    if not user:
        verify_password_hash(password, settings.DUMMY_HASH)
        return False
    if not verify_password_hash(password, user.password_hash):
        return False
    return user

