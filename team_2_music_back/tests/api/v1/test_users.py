import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_read_users_me(authorized_client: AsyncClient):
    response = await authorized_client.get("/api/v1/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["nickname"] == "testuser"

@pytest.mark.asyncio
async def test_update_user_profile(authorized_client: AsyncClient):
    # First ensure user exists (handled by get_current_active_user in the dependency chain)
    
    update_data = {
        "nickname": "updated_nickname",
        "bio": "I am a test user"
    }
    
    response = await authorized_client.patch("/api/v1/users/me", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["nickname"] == "updated_nickname"
    assert data["bio"] == "I am a test user"
    
    # Verify persistence
    response = await authorized_client.get("/api/v1/users/me")
    assert response.json()["nickname"] == "updated_nickname"
