from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_database
from app.schemas.user import UserCreateSchema, UserReadSchema
from app.services.auth_service import register_user


auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@auth_router.post("/register", response_model=UserReadSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, db: Session = Depends(get_database),):
    return register_user(db, user_data)