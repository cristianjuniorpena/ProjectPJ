
import os

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.base import Base
from app.api.dependencies import get_database

# Importar os modelos para registrar suas tabelas no metadata
from app.models.user import User
from app.models.post import Post


TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError(
        "TEST_DATABASE_URL não foi configurada."
    )

if "platform_pj_test" not in TEST_DATABASE_URL:
    raise RuntimeError(
        "A URL não aponta para o banco de testes esperado."
    )


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Cria as tabelas no banco exclusivo de testes
    Base.metadata.create_all(bind=engine)

    yield

    # Remove as tabelas ao terminar a execução
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture
def database():
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(database):

    def override_get_database():
        yield database

    app.dependency_overrides[get_database] = override_get_database

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()