
from sqlalchemy.orm import Session

from app.crud.crud_user import select_user, select_users_in_database,delete_user_in_database

from app.models.user import User

from app.exceptions.user_exceptions import UserNotFound, UserDeletionConflictError



def read_user(database: Session, user_id: int) -> User:
    user = select_user(database, user_id)

    if user is None:
        raise UserNotFound("User not found")

    return user

def list_users(database: Session, limit: int = 100, offset: int = 0) -> list[User]:
    users = select_users_in_database(database=database, limit=limit, offset=offset)
    return users

def remove_user(database: Session, user_id: int) -> None:
    read_user(database, user_id)

    deleted = delete_user_in_database(database=database, user_id=user_id)

    if not deleted:
        raise UserNotFound("User not found")
