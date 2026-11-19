from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.user import User

def get_id_by_email(database: Session, email):
    query = database.execute(select(User.id).where(User.email == email))
    user_id = query.scalars().first()
    return user_id

def get_users_in_database(database: Session):
    query = database.execute(select(User))
    all_users = query.scalars().all()
    return all_users

def get_user(database: Session, id: str):
    query = database.execute(select(User).where(User.id == id))
    user = query.scalars().first()
    return user

def delete_user_in_database(database: Session, id: int):
    database.execute(delete(User).where(User.id == id))
    database.commit()
    return True

def insert_user_in_database(database: Session, user: User) -> User:
    try:
        database.add(user)
        database.commit()
        database.refresh(user)

    except IntegrityError as error:
        database.rollback()

        constraint_name = getattr(
            getattr(error.orig, "diag", None),
            "constraint_name",
            None,
        )

        if constraint_name == "uq_users_email":
            raise HTTPException(
                status_code=409,
                detail="Email already registered",
            ) from error

        raise
    
    return user