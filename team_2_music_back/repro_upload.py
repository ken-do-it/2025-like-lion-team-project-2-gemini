import asyncio
from app.api.v1.endpoints.tracks import finalize_upload
from app.schemas import schemas
from app.db.database import SessionLocal
from unittest.mock import MagicMock

async def test_finalize():
    db = SessionLocal()
    
    # Mock request
    request = schemas.UploadFinalizeRequest(
        upload_id="test-upload-id",
        title="Test Track",
        description="Test Description",
        tags=[],
        cover_image_url=None
    )
    
    # Mock current_user (simulating get_optional_user result)
    current_user = {
        "user_id": "test_user_123",
        "email": "test@example.com"
        # db_user is missing initially
    }
    
    try:
        print("Calling finalize_upload...")
        result = await finalize_upload(request, current_user, db)
        print("Success:", result)
    except Exception as e:
        print("Error occurred:")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(test_finalize())
