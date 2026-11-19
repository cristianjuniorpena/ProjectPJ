from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.schemas.auth import TokenResponse
from datetime import timedelta

from app.api.dependencies import get_database, get_current_user
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.auth_service import register_user, authenticate_user
from app.core.config import settings
from app.core.security import create_access_token, create_payload_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, database: Session = Depends(get_database),):
    return register_user(database, user_data)

@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: Session = Depends(get_database)) -> TokenResponse:
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    payload = create_payload_token(user_id=user.id, email=user.email)
    access_token = create_access_token(payload=payload)
    return TokenResponse(access_token=access_token, token_type="bearer")