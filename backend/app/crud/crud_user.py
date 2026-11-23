
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.user import User
from app.exceptions.user_exceptions import UserAlreadyExistsError, UserDeletionConflictError





def get_id_by_email(database: Session, email: str) -> int | None:
    statement = select(User.id).where(User.email == email)
    return database.scalar(statement)


def get_users_in_database(
    database: Session,
    limit: int = 100,
    offset: int = 0
) -> list[User]:

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")

    if offset < 0:
        raise ValueError("Offset cannot be negative")

    statement = (
        select(User)
        .order_by(User.id)
        .limit(limit)
        .offset(offset)
    )

    return list(database.scalars(statement).all())


def get_user(database: Session, user_email: int) -> User | None:
    return database.get(User, user_email)


def delete_user_in_database(
    database: Session,
    user_id: int
) -> bool:

    user = database.get(User, user_id)

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


def insert_user_in_database(
    database: Session,
    user: User
) -> User:

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

def update_user_in_database(
    database: Session,
    user_id: int,
    update_data: dict
) -> User | None:

    user = database.get(User, user_id)

    if user is None:
        return None

    allowed_fields = {"name", "email"}

    invalid_fields = set(update_data.keys()) - allowed_fields

    if invalid_fields:
        raise ValueError(
            f"Fields cannot be updated: {invalid_fields}"
        )

    if not update_data:
        return user

    try:
        for field, value in update_data.items():
            setattr(user, field, value)

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
            raise UserAlreadyExistsError() from error

        raise

    except SQLAlchemyError:
        database.rollback()
        raise

    return user
