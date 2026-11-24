from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import oauth2_scheme
from app.crud.crud_user import select_user
from app.database.session import SessionLocal
from app.models.user import User
from app.schemas.auth import TokenData

credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

def get_database() -> Generator[Session, None, None]:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], database: Annotated[Session, Depends(get_database)]) -> User:  
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenData(user_id=int(payload["sub"]), email=payload.get("email"))
    except (InvalidTokenError, KeyError, TypeError, ValueError):
        raise credentials_exception from None
    user = select_user(database, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception

    return user 
