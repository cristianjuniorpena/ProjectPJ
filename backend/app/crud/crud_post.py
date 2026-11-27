from decimal import Decimal
from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.models.post import Post
from app.exceptions.post_exceptions import PostDeletionConflictError



def select_all_posts(
    database: Session,
    limit: int = 20,
    offset: int = 0,
    category: str | None = None,
    status: str | None = None,
    search: str | None = None,
    min_budget: Decimal | None = None,
    max_budget: Decimal | None = None
) -> list[Post]:

    if not 1 <= limit <= 100:
        raise ValueError("Limit must be between 1 and 100")

    if offset < 0:
        raise ValueError("Offset cannot be negative")

    statement = (
        select(Post)
        .options(joinedload(Post.user))
    )

    if category:
        statement = statement.where(
            Post.category.ilike(f"%{category.strip()}%")
        )

    if status:
        statement = statement.where(Post.status == status)

    if search:
        search_term = f"%{search.strip()}%"
        statement = statement.where(
            or_(
                Post.title.ilike(search_term),
                Post.description.ilike(search_term)
            )
        )

    if min_budget is not None:
        statement = statement.where(Post.budget >= min_budget)

    if max_budget is not None:
        statement = statement.where(Post.budget <= max_budget)

    statement = (
        statement
        .order_by(Post.created_at.desc(), Post.id.desc())
        .limit(limit)
        .offset(offset)
    )

    return list(database.scalars(statement).all())


def select_user_posts(database: Session, user_id: int) -> list[Post] | None:
    query = select(Post).where(Post.user_id == user_id).order_by(Post.created_at.desc())
    return database.scalars(query).all()

def select_post(database: Session, post_id: int) -> Post | None:
    if post_id <= 0:
        return None
    return database.get(Post, post_id)


def insert_post(database: Session, post: Post) -> Post:
    try:
        database.add(post)
        database.commit()
        database.refresh(post)
    except IntegrityError:
        database.rollback()
        raise
    except SQLAlchemyError:
        database.rollback()
        raise

    return post

def verify_invalid_fields(update_data: dict) -> bool:
    allowed_fields = {
            "title",
            "description",
            "category",
            "budget",
            "status"
        }

    invalid_fields = set(update_data.keys()) - allowed_fields

    if invalid_fields:
        return True
    return False


def update_post(database: Session, post_id: int, update_data: dict) -> Post | None:

    post = select_post(database=database, post_id=post_id)
    if post is None:
        return None

    if verify_invalid_fields(update_data):
        raise ValueError("não se pode alterar campos inválidos")

    if not update_data:
        return post

    try:
        for field, value in update_data.items():
            setattr(post, field, value)
        database.commit()
        database.refresh(post)
    except IntegrityError:
        database.rollback()
        raise
    except SQLAlchemyError:
        database.rollback()
        raise

    return post


def delete_post(database: Session, post_id: int) -> bool:

    post = select_post(database=database,post_id=post_id)
    if post is None:
        return False

    try:
        database.delete(post)
        database.commit()
    except IntegrityError as error:
        database.rollback()
        raise PostDeletionConflictError(
            "Post cannot be deleted because of a database constraint."
        ) from error
    except SQLAlchemyError:
        database.rollback()
        raise

    return True
