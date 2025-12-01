import pytest
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.orm import Session

from app.main import app
from app.db.database import get_db, SessionLocal, engine, Base
from app.api.dependencies import get_current_user, get_optional_user

# Setup database tables before tests
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# Database Session Fixture
@pytest.fixture(scope="function")
def db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Async Client Fixture
@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c

# Mock User Fixture
@pytest.fixture
def mock_user_data():
    return {
        "user_id": "test-user-id",
        "email": "test@example.com",
        "nickname": "testuser",
        "roles": ["user"],
        "db_user_id": 1
    }

# Override Dependency Fixture
@pytest.fixture
async def authorized_client(client: AsyncClient, mock_user_data, db: Session) -> AsyncGenerator[AsyncClient, None]:
    # Create a test user in the database
    from app.crud import crud
    from app.schemas import schemas
    
    # Check if user exists, if not create
    test_user = crud.get_user_profile_by_user_id(db, "test-user-id")
    if not test_user:
        test_user = crud.create_user_profile(db, schemas.UserProfileCreate(
            user_id="test-user-id",
            nickname="testuser"
        ))
    
    # Update mock_user_data with actual db_user_id
    mock_user_data["db_user_id"] = test_user.id
    mock_user_data["db_user"] = test_user
    
    async def mock_get_current_user():
        return mock_user_data
    
    app.dependency_overrides[get_current_user] = mock_get_current_user
    app.dependency_overrides[get_optional_user] = mock_get_current_user
    yield client
    app.dependency_overrides.clear()
