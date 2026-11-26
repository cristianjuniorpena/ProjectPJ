from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, load_only

from app.models.user import User
from app.schemas.user import UserReadSchema
from app.exceptions.user_exceptions import UserAlreadyExistsError, UserDeletionConflictError


def select_user_by_email(database: Session, user_email: str):
    query = select(User).where(User.email == user_email)
    return database.execute(query).scalar()

def select_user(database: Session, user_id: int) -> User | None:
    return database.get(User, user_id)

def select_users_in_database(database: Session, limit: int = 100, offset: int = 0) -> list[User]:
    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")

    if offset < 0:
        raise ValueError("Offset cannot be negative")

    fields_user_read_schema = [getattr(User, field) for field in UserReadSchema.model_fields.keys()]

    statement = (
        select(User)
        .options(load_only(*fields_user_read_schema))
        .order_by(User.id)
        .limit(limit)
        .offset(offset)
    )

    return list(database.scalars(statement).all())

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
            raise UserAlreadyExistsError(
                "Email already registered"
            ) from error

        raise

    except SQLAlchemyError:
        database.rollback()
        raise

    return user

def delete_user_in_database(database: Session, user_id: int) -> bool:
    user = select_user(database=database, user_id=user_id)
    if user is None:
        return False

    try:
        database.delete(user)
        database.commit()

    except IntegrityError as error:
        database.rollback()

        raise UserDeletionConflictError(
            "User cannot be deleted because it has related records."
        ) from error

    except SQLAlchemyError:
        database.rollback()
        raise

    return True



