from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import get_database
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.auth_service import register_user, authenticate_user
from app.core.security import create_access_token, create_payload_token

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

database_dependencie = Annotated[Session, Depends(get_database)]

@auth_router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateSchema, database: database_dependencie):
    return register_user(database, user_data)

@auth_router.post('/login', response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], database: database_dependencie) -> TokenResponse:
    user = authenticate_user(database, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = create_payload_token(user_id=user.id, email=user.email)
    access_token = create_access_token(payload=payload)
    return TokenResponse(access_token=access_token, token_type="bearer")