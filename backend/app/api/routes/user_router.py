from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencies import get_database
from app.services.auth_user import authenticate_user
from app.crud.crud_user import get_user, get_users_from_database, delete_user_from_database, get_id_by_email


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

@user_router.delete('/delete', status_code=status.HTTP_200_OK)
async def delete_user(database: Session = Depends(get_database), email: str | None = None):
    if email == None:
        raise HTTPException()
    user_id = get_id_by_email(database, email)
    delete_user_from_database(database, user_id)
    return {
        'status' : 'sucesso',
        'mensagem' : f'usuario de id {user_id} deletado'
    }