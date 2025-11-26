import pytest
import asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient
from sqlalchemy.orm import Session

from app.main import app
from app.db.database import get_db, SessionLocal
from app.api.dependencies import get_current_user

# Event Loop Fixture
@pytest.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Database Session Fixture
@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()

# Async Client Fixture
@pytest.fixture
async def client() -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as c:
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
@pytest.fixture
def authorized_client(client: AsyncClient, mock_user_data) -> AsyncClient:
    async def mock_get_current_user():
        return mock_user_data
    
    app.dependency_overrides[get_current_user] = mock_get_current_user
    return client
