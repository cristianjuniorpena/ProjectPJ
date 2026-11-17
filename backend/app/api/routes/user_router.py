from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencies import get_database
from app.services.auth_service import register_user
from app.services.auth_user import get_users_from_database
from app.models.user import User


user_router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@user_router.get('/', status_code=status.HTTP_200_OK)
def get_users():
    all_users = get_users_from_database()
    return {
        'status' : 'ok',
        'users' : all_users
        }   