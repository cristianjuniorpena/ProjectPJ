
from sqlalchemy.orm import Session

from app.crud.crud_user import get_user, get_users_in_database,delete_user_in_database

from app.models.user import User

from app.exceptions.user_exceptions import UserNotFound, UserDeletionConflictError



def read_user(database: Session, user_id: int) -> User:
    user = get_user(database, user_id)

    if user is None:
        raise UserNotFound("User not found")

    return user

def list_users(database: Session, limit: int = 100, offset: int = 0) -> list[User]:
    users = get_users_in_database(database=database, limit=limit, offset=offset)
    return users

# def edit_user(database: Session, user_id: int, update_data: dict) -> User:

#     read_user(database, user_id)
#     if "email" in update_data and update_data["email"] is not None:
#         update_data["email"] = normalize_email(update_data["email"])

#     updated_user = update_user_in_database(database=database, user_id=user_id, update_data=update_data)

#     if updated_user is None:
#         raise UserNotFound("User not found")

#     return updated_user

def remove_user(database: Session, user_id: int) -> None:
    read_user(database, user_id)

    deleted = delete_user_in_database(database=database, user_id=user_id)

    if not deleted:
        raise UserNotFound("User not found")
