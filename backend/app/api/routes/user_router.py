from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencies import get_database
from app.services.auth_service import register_user
from app.models.user import User

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.get('/', status_code=status.HTTP_200_OK)
def get_users(database: Session = Depends(get_database)):
    result = database.execute(select(User))
    all_users = result.scalars().all()
    return {
        'status' : 'ok',
        'users' : all_users
        }