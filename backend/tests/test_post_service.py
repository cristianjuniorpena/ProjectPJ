
import pytest

from app.models.user import User
from app.models.post import Post

from app.schemas.post import PostCreate, PostUpdate

from app.crud.crud_user import insert_user_in_database
from app.crud.crud_post import insert_post

from app.services.post_service import (
    instantiate_post,
    list_posts,
    read_post,
    read_current_user_posts,
    create_post,
    edit_post,
    remove_post,
)

from app.exceptions.post_exceptions import (
    PostNotFoundError,
    PostPermissionError,
    PostRoleError,
)


# ---------- Funções auxiliares ----------

def create_test_user(database, email, role="contractor"):
    user = User(
        name="Usuário Teste",
        email=email,
        password_hash="hash_de_teste",
        role=role,
    )

    return insert_user_in_database(database=database, user=user)


def create_test_post(database, user_id, **overrides):
    data = {
        "user_id": user_id,
        "title": "Desenvolvimento de API",
        "description": "Preciso de uma API para um pequeno projeto.",
        "category": "Programação",
    }

    data.update(overrides)

    post = Post(**data)

    return insert_post(database=database, post=post)


# ---------- INSTANTIATE ----------

def test_instantiate_post(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    post_data = PostCreate(
        title="Desenvolvimento de API",
        description="Preciso de uma API.",
        category="Programação",
    )

    post = instantiate_post(
        post_data=post_data,
        current_user=user,
    )

    assert post.title == post_data.title
    assert post.description == post_data.description
    assert post.category == post_data.category
    assert post.user_id == user.id
    assert post.status == "open"
    assert post.budget is None


# ---------- LIST POSTS ----------

def test_list_posts(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    create_test_post(database, user.id)

    results = list_posts(database=database)

    assert len(results) == 1
    assert results[0].user_id == user.id


# ---------- READ POST ----------

def test_read_post(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    post = create_test_post(database, user.id)

    result = read_post(
        database=database,
        post_id=post.id,
    )

    assert result.id == post.id
    assert result.title == post.title


def test_read_post_not_found(database):
    with pytest.raises(PostNotFoundError):
        read_post(
            database=database,
            post_id=999999,
        )


# ---------- READ CURRENT USER POSTS ----------

def test_read_current_user_posts(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    create_test_post(database, user.id)

    results = read_current_user_posts(
        database=database,
        current_user=user,
    )

    assert len(results) == 1
    assert results[0].user_id == user.id


def test_read_current_user_posts_provider(database):
    user = create_test_user(
        database,
        email="provider@email.com",
        role="provider",
    )

    with pytest.raises(PostRoleError):
        read_current_user_posts(
            database=database,
            current_user=user,
        )


# ---------- CREATE POST ----------

def test_create_post(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    post_data = PostCreate(
        title="Desenvolvimento de API",
        description="Preciso de uma API.",
        category="Programação",
    )

    result = create_post(
        database=database,
        post_data=post_data,
        current_user=user,
    )

    assert result.id is not None
    assert result.user_id == user.id
    assert result.title == post_data.title
    assert result.status == "open"


def test_create_post_provider(database):
    user = create_test_user(
        database,
        email="provider@email.com",
        role="provider",
    )

    post_data = PostCreate(
        title="Desenvolvimento de API",
        description="Preciso de uma API.",
        category="Programação",
    )

    with pytest.raises(PostRoleError):
        create_post(
            database=database,
            post_data=post_data,
            current_user=user,
        )


# ---------- EDIT POST ----------

def test_edit_own_post(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    post = create_test_post(database, user.id)

    update_data = PostUpdate(
        title="Título atualizado",
    )

    result = edit_post(
        database=database,
        post_id=post.id,
        post_data=update_data,
        current_user=user,
    )

    assert result.title == "Título atualizado"
    assert result.id == post.id


def test_edit_post_owned_by_another_user(database):
    owner = create_test_user(
        database,
        email="owner@email.com",
    )

    another_user = create_test_user(
        database,
        email="another@email.com",
    )

    post = create_test_post(database, owner.id)

    with pytest.raises(PostPermissionError):
        edit_post(
            database=database,
            post_id=post.id,
            post_data=PostUpdate(title="Tentativa de alteração"),
            current_user=another_user,
        )


def test_provider_cannot_edit_post(database):
    owner = create_test_user(
        database,
        email="owner@email.com",
    )

    provider = create_test_user(
        database,
        email="provider@email.com",
        role="provider",
    )

    post = create_test_post(database, owner.id)

    with pytest.raises(PostRoleError):
        edit_post(
            database=database,
            post_id=post.id,
            post_data=PostUpdate(title="Tentativa de alteração"),
            current_user=provider,
        )


def test_edit_post_not_found(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    with pytest.raises(PostNotFoundError):
        edit_post(
            database=database,
            post_id=999999,
            post_data=PostUpdate(title="Novo título"),
            current_user=user,
        )


# ---------- REMOVE POST ----------

def test_remove_own_post(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    post = create_test_post(database, user.id)

    result = remove_post(
        database=database,
        post_id=post.id,
        current_user=user,
    )

    assert result.id == post.id


def test_remove_post_owned_by_another_user(database):
    owner = create_test_user(
        database,
        email="owner@email.com",
    )

    another_user = create_test_user(
        database,
        email="another@email.com",
    )

    post = create_test_post(database, owner.id)

    with pytest.raises(PostPermissionError):
        remove_post(
            database=database,
            post_id=post.id,
            current_user=another_user,
        )


def test_provider_cannot_remove_post(database):
    owner = create_test_user(
        database,
        email="owner@email.com",
    )

    provider = create_test_user(
        database,
        email="provider@email.com",
        role="provider",
    )

    post = create_test_post(database, owner.id)

    with pytest.raises(PostRoleError):
        remove_post(
            database=database,
            post_id=post.id,
            current_user=provider,
        )


def test_remove_post_not_found(database):
    user = create_test_user(
        database,
        email="contractor@email.com",
    )

    with pytest.raises(PostNotFoundError):
        remove_post(
            database=database,
            post_id=999999,
            current_user=user,
        )
