from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.dependencies import get_database, get_current_user
from app.crud.crud_user import get_users_in_database, delete_user_in_database, get_id_by_email
from app.models.user import User
from app.schemas.user import UserReadSchema


user_router = APIRouter(
    prefix="/user",
    tags=["users"],
)



@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_all_users(database: Session = Depends(get_database)):
    all_users = get_users_in_database(database)
    return {
        'status' : 'ok',
        'users' : all_users
        }   

@user_router.get('/me', response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]) -> User:
    return current_user

@user_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(database: Session = Depends(get_database), current_user: User = Depends(get_current_user)):
    delete_user_in_database(database, current_user.id)
    return {
        'status' : 'sucesso',
        'mensagem' : f'usuario de id {current_user.id} deletado'
    }