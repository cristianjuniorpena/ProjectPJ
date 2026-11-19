from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated

from sqlalchemy.orm import Session
from collections.abc import Generator

from app.database.session import SessionLocal
from app.core.config import settings
from app.schemas.auth import TokenResponse
from app.crud.crud_user import get_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_database() -> Generator[Session, None, None]:
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()

token_router = APIRouter(
    prefix="/token",
    tags=["router for tokens"],
)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], database: Session = Depends(get_database)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenResponse(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(database, user_id=token_data.access_token)
    if user is None:
        raise credentials_exception
    return user

