
from typing import Annotated, Literal

from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from sqlalchemy.orm import Session

from app.api.dependencies import get_database, get_current_user
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate, PostRead, PostReadAllPosts
from app.services.post_service import list_posts, read_post, read_current_user_posts,create_post, edit_post, remove_post
from app.exceptions.post_exceptions import PostNotFoundError, PostPermissionError, PostRoleError, PostDeletionConflictError, MinBudgetExceedMaxBudget



post_router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)


database_dependencie = Annotated[Session, Depends(get_database)]
current_user_dependencie = Annotated[User, Depends(get_current_user)]



@post_router.get("/", response_model=list[PostRead], status_code=200)
def get_all_posts(
    database: database_dependencie,
    current_user: current_user_dependencie,
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    category: str | None = Query(default=None, min_length=2, max_length=100),
    status: Literal["open", "closed"] | None = None,
    search: str | None = Query(default=None, min_length=1, max_length=150),
    min_budget: Decimal | None = Query(default=None, ge=0),
    max_budget: Decimal | None = Query(default=None, ge=0)
):

    try:
        return list_posts(
            database=database,
            limit=limit,
            offset=offset,
            category=category,
            status=status,
            search=search,
            min_budget=min_budget,
            max_budget=max_budget
        )
    except MinBudgetExceedMaxBudget:
        raise HTTPException(
            status_code=422,
            detail="Minimum budget cannot exceed maximum budget"
        )


@post_router.get("/my-posts", response_model=list[PostRead], status_code=status.HTTP_200_OK)
def get_my_posts(database: database_dependencie, current_user: current_user_dependencie):
    try:
        return read_current_user_posts(database=database, current_user=current_user)
    except PostRoleError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )

@post_router.get("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def get_post(database: database_dependencie, post_id: int):
    try:
        return read_post(database, post_id)

    except PostNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

@post_router.post("/", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_new_post(post_data: PostCreate, database: database_dependencie, current_user: current_user_dependencie):
    try:
        return create_post(database, post_data, current_user)
    except PostRoleError as error:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(error)
        )


@post_router.patch("/{post_id}", response_model=PostRead, status_code=status.HTTP_200_OK)
def update_existing_post(post_id: int, post_data: PostUpdate, database: database_dependencie, current_user: current_user_dependencie):
    try:
        return edit_post(database=database, post_id=post_id, post_data=post_data, current_user=current_user)
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


@post_router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_post(post_id: int, database: database_dependencie, current_user: current_user_dependencie):
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