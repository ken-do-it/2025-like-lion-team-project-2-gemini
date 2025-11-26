import pytest
from httpx import AsyncClient
from unittest.mock import patch, MagicMock

@pytest.mark.asyncio
async def test_initiate_upload(authorized_client: AsyncClient):
    with patch("boto3.client") as mock_boto:
        mock_s3 = MagicMock()
        mock_boto.return_value = mock_s3
        mock_s3.generate_presigned_url.return_value = "https://s3.example.com/presigned-url"
        
        payload = {
            "filename": "test_song.mp3",
            "content_type": "audio/mpeg",
            "file_size": 1024 * 1024 * 5
        }
        
        response = await authorized_client.post("/api/v1/tracks/upload/initiate", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "upload_id" in data
        assert data["presigned_url"] == "https://s3.example.com/presigned-url"

@pytest.mark.asyncio
async def test_read_tracks(client: AsyncClient):
    response = await client.get("/api/v1/tracks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_upload_finalize_flow(authorized_client: AsyncClient):
    # 1. Initiate (Mocked)
    upload_id = "test-upload-id"
    
    # 2. Finalize
    finalize_payload = {
        "upload_id": upload_id,
        "title": "My New Song",
        "description": "A test song description",
        "cover_image_url": "http://example.com/cover.jpg"
    }
    
    response = await authorized_client.post("/api/v1/tracks/upload/finalize", json=finalize_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "My New Song"
    assert data["artist_name"] == "testuser"
    
    # 3. Verify it appears in list
    response = await authorized_client.get(f"/api/v1/tracks/{data['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "My New Song"
