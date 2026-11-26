import os
from dotenv import load_dotenv

import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database.base import Base
from app.api.dependencies import get_database

load_dotenv()



TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    raise RuntimeError("TEST_DATABASE_URL não foi configurada.")

database_url = make_url(TEST_DATABASE_URL)

if database_url.database != "platform_pj_test":
    raise RuntimeError("A URL não aponta para o banco de testes.")

if database_url.host not in ("localhost", "127.0.0.1"):
    raise RuntimeError("O banco de testes deve ser local.")


engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    join_transaction_mode="create_savepoint"
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)

    yield

    engine.dispose()


@pytest.fixture
def database():
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(database):

    def override_get_database():
        yield database

    app.dependency_overrides[get_database] = override_get_database

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
