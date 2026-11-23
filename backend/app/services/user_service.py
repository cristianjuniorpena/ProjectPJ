from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from app.api.dependencies import get_database, get_current_user
from app.crud.crud_user import get_users_in_database, delete_user_in_database, get_id_by_email
from app.models.user import User
from app.schemas.user import UserReadSchema


def exclude_user():
    print('oi')