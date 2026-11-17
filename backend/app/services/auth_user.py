from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.crud.crud_user import get_user
from app.core.security import verify_password_hash
from app.core.config import settings

def authenticate_user(database: Session, email: str, password: str):
    user = get_user(database, email)
    if not user:
        verify_password_hash(password, settings.DUMMY_HASH)
        return False
    if not verify_password_hash(password, user.password_hash):
        return False
    return user

