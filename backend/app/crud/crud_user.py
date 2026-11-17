from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User

def get_id_by_email(database: Session, email):
    query = database.execute(select(User.id).where(User.email == email))
    user_id = query.scalars().first()
    return user_id

def get_users_from_database(database: Session):
    query = database.execute(select(User))
    all_users = query.scalars().all()
    return all_users

def get_user(database: Session, email: str):
    query = database.execute(select(User).where(User.email == email))
    user = query.scalars().first()
    return user

def delete_user_from_database(database: Session, id: int):
    database.execute(delete(User).where(User.id == id))
    database.commit()
    return True