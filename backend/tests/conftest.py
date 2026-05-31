import os
from typing import Any
from typing import Generator

import asyncpg
import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from backend.core.db_helper import db_helper
from backend.main import app
from backend.core.config import BASE_DIR
from backend.core.config import settings

CLEAN_TABLES = [
    "client",
    "company",
    "token",
    "service",
]


@pytest.fixture(scope="session", autouse=True)
async def run_migrations(async_session_test):
    migration_tests: str = os.path.join(BASE_DIR, "tests", "alembic.ini")
    os.system(f"alembic --config {migration_tests} upgrade head")
    yield
    async with async_session_test() as session:
        async with session.begin():
            for table_for_cleaning in CLEAN_TABLES:
                await session.execute(
                    text(f"TRUNCATE TABLE {table_for_cleaning} CASCADE;")
                )


@pytest.fixture(scope="session")
async def async_session_test():
    engine = create_async_engine(settings.db_test.url, future=True, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    yield async_session


async def _get_test_db():
    try:
        # create async engine for interaction with database
        test_engine = create_async_engine(settings.db_test.url, future=True, echo=True)

        # create session for the interaction with database
        test_async_session = sessionmaker(
            test_engine, expire_on_commit=False, class_=AsyncSession
        )
        yield test_async_session()
    finally:
        pass


@pytest.fixture(scope="session")
async def client() -> Generator[TestClient, Any, None]:
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """
    app.dependency_overrides[db_helper.session_getter] = _get_test_db
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="session")
async def asyncpg_pool():
    pool = await asyncpg.create_pool(settings.db_test.url)
    yield pool
    pool.close()


@pytest.fixture(scope="session")
async def auth_header(client):
    resp = client.post(
        "/api/v1/company/auth/register",
        json={
            "name": "Tesla",
            "address": "string",
            "email": "ElonMask123@example.com",
            "phone": "+79126329304",
            "password": "Pass312!",
            "repeatPassword": "Pass312!",
        },
    )
    print(resp.json())
    access_token = resp.json()["accessToken"]
    token = f"Bearer {access_token}"

    return {"Authorization": token}
