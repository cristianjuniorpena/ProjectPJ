from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.dependencies import get_database, get_current_user
from app.services.user_service import read_user, list_users, remove_user
from app.models.user import User
from app.schemas.user import UserReadSchema


user_router = APIRouter(
    prefix="/user",
    tags=["users"],
)

database_dependencie = Annotated[Session, Depends(get_database)]
current_user_dependencie = Annotated[User, Depends(get_current_user)]

@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_all_users(database: database_dependencie):
    all_users = get_users_in_database(database)
    return {
        'status' : 'ok',
        'users' : all_users
        }   

@user_router.get('/me', response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def read_user_me(current_user: current_user_dependencie) -> User:
    return current_user

@user_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(database: database_dependencie, current_user: current_user_dependencie):
    removed_user = remove_user(database=database, user_id=current_user.id)
    return {
        'status' : 'sucesso',
        'mensagem' : f'usuario de id {current_user.id} deletado'
    }