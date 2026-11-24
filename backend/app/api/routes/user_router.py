from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.dependencies import get_database, get_current_user
from app.services.user_service import list_users, remove_user
from app.models.user import User
from app.schemas.user import UserReadSchema
from app.exceptions.user_exceptions import UserDeletionConflictError



user_router = APIRouter(
    prefix="/user",
    tags=["users"],
)

database_dependencie = Annotated[Session, Depends(get_database)]
current_user_dependencie = Annotated[User, Depends(get_current_user)]

@user_router.get('/', status_code=status.HTTP_200_OK)
async def get_all_users(database: database_dependencie):
    all_users = list_users(database)
    return {
        'status' : 'ok',
        'users' : all_users
        }   

@user_router.get('/me', response_model=UserReadSchema, status_code=status.HTTP_200_OK)
async def read_user_me(current_user: current_user_dependencie) -> User:
    return current_user

@user_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(database: database_dependencie, current_user: current_user_dependencie):
    try:
        remove_user(database=database, user_id=current_user.id)
    except UserDeletionConflictError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{error}"
        )
    return {
        'status' : 'sucesso',
        'mensagem' : f'usuario de id {current_user.id} deletado'
    }