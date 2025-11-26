import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import Session

from app.main import app
from app.db.database import get_db, SessionLocal, engine, Base
from app.api.dependencies import get_current_user

# Setup database tables before tests
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Event Loop Fixture
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Database Session Fixture
@pytest.fixture(scope="function")
def db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async Client Fixture
@pytest_asyncio.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

# Mock User Fixture
@pytest.fixture
def mock_user_data():
    return {
        "user_id": "test-user-id",
        "email": "test@example.com",
        "nickname": "testuser",
        "roles": ["user"]
    }

# Override Dependency Fixture
@pytest_asyncio.fixture
async def authorized_client(client: AsyncClient, mock_user_data) -> AsyncClient:
    async def mock_get_current_user():
        return mock_user_data
    
    app.dependency_overrides[get_current_user] = mock_get_current_user
    yield client
    app.dependency_overrides.clear()

