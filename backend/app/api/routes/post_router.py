
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_database,
    get_current_user
)

from app.models.user import User

from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostRead
)

from app.services.post_service import (
    list_posts,
    read_post,
    create_post,
    edit_post,
    remove_post
)

from app.exceptions.post_exceptions import (
    PostNotFoundError,
    PostPermissionError,
    PostRoleError,
    PostDeletionConflictError
)


post_router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


DatabaseDep = Annotated[Session, Depends(get_database)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]


@post_router.get(
    "/",
    response_model=list[PostRead],
    status_code=status.HTTP_200_OK
)
def get_all_posts(
    database: DatabaseDep,
    current_user: CurrentUserDep,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    return list_posts(database, limit, offset)


@post_router.get(
    "/{post_id}",
    response_model=PostRead,
    status_code=status.HTTP_200_OK
)
def get_post(
    post_id: int,
    database: DatabaseDep,
    current_user: CurrentUserDep
):
    try:
        return read_post(database, post_id)

    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )


@post_router.post(
    "/",
    response_model=PostRead,
    status_code=status.HTTP_201_CREATED
)
def create_new_post(
    post_data: PostCreate,
    database: DatabaseDep,
    current_user: CurrentUserDep
):
    try:
        return create_post(database, post_data, current_user)

    except PostRoleError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )


@post_router.patch(
    "/{post_id}",
    response_model=PostRead,
    status_code=status.HTTP_200_OK
)
def update_existing_post(
    post_id: int,
    post_data: PostUpdate,
    database: DatabaseDep,
    current_user: CurrentUserDep
):
    try:
        return edit_post(
            database,
            post_id,
            post_data,
            current_user
        )

    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    except (PostPermissionError, PostRoleError) as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )


@post_router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_existing_post(
    post_id: int,
    database: DatabaseDep,
    current_user: CurrentUserDep
):
    try:
        remove_post(database, post_id, current_user)

    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    except (PostPermissionError, PostRoleError) as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )

    except PostDeletionConflictError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Post cannot be deleted due to related records"
        )

    return None
