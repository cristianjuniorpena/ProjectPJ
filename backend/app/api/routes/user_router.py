from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.dependencies import get_database
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.auth_service import register_user
from app.models.user import User

router = APIRouter(
    prefix="/user",
    tags=["users"],
)


@router.get('/')
def get_users(database: Session = Depends(get_database)):
    all_users = database.execute(select(User)).all()
    return {'users' : all_users}