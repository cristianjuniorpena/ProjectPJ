
from sqlalchemy.orm import Session

from app.crud.crud_post import select_all_posts, select_post, select_user_posts,insert_post, update_post, delete_post

from app.models.post import Post
from app.models.user import User

from app.schemas.post import PostCreate, PostUpdate

from app.exceptions.post_exceptions import PostNotFoundError, PostPermissionError, PostRoleError

def instantiate_post(post_data: PostCreate, current_user: User):
    post = Post(
        title=post_data.title,
        description=post_data.description,
        category=post_data.category,
        budget=post_data.budget,
        user_id=current_user.id,
        status="open"
    )
    return post

def list_posts(database: Session, limit: int = 100, offset: int = 0) -> list[Post]:
    return select_all_posts(database, limit, offset)

def read_post(database: Session, post_id: int) -> Post:
    post = select_post(database, post_id)
    if post is None:
        raise PostNotFoundError()
    return post

def read_current_user_posts(database: Session, current_user: User) -> list[Post]:
    if current_user.role != "contractor":
         raise PostRoleError(
            "Only contractors can create posts."
        )
    return select_user_posts(database=database, user_id=current_user.id)

def create_post(database: Session, post_data: PostCreate, current_user: User) -> Post:
    if current_user.role != "contractor":
        raise PostRoleError(
            "Only contractors can create posts."
        )

    post = instantiate_post(post_data=post_data, current_user=current_user)

    return insert_post(database, post)


def edit_post(database: Session, post_id: int, post_data: PostUpdate, current_user: User) -> Post:
    post = read_post(database, post_id)

    if post.user_id != current_user.id:
        raise PostPermissionError(
            "You cannot modify another user's post."
        )

    if current_user.role != "contractor":
        raise PostRoleError(
            "Only contractors can modify posts."
        )

    update_data = post_data.model_dump(exclude_unset=True)

    updated_post = update_post(database, post_id, update_data)

    if updated_post is None:
        raise PostNotFoundError()

    return updated_post


def remove_post(database: Session, post_id: int, current_user: User) -> bool:
    post = read_post(database, post_id)

    if post.user_id != current_user.id:
        raise PostPermissionError(
            "You cannot delete another user's post."
        )

    if current_user.role != "contractor":
        raise PostRoleError(
            "Only contractors can delete posts."
        )

    deleted = delete_post(database, post_id)

    if not deleted:
        raise PostNotFoundError()

    return post
