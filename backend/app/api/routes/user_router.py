from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencies import get_database
from app.services.auth_user import get_users_from_database, authenticate_user


user_router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_all_users(database: Session = Depends(get_database)):
    all_users = get_users_from_database(database)
    return {
        'status' : 'ok',
        'users' : all_users
        }   

@user_router.get('/me', status_code=status.HTTP_200_OK)
async def get_current_user(database: Session = Depends(get_database)):
    all_users = authenticate_user(database, 'contratante@email.com', 'contratante123')
    return {
        'status' : 'ok',
        'users' : all_users
        }   