from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from typing import List
import boto3
from botocore.exceptions import ClientError
import uuid
import os
from pathlib import Path
from datetime import datetime

from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.core.config import settings
from app.api.dependencies import get_current_active_user, get_optional_user
from app.core.exceptions import ResourceNotFoundError, ValidationError

router = APIRouter()

@router.post("/upload/initiate", response_model=schemas.UploadInitiateResponse)
async def initiate_upload(
    request: schemas.UploadInitiateRequest,
    current_user: dict = Depends(get_current_active_user)
):
    """
    음악 업로드를 시작하고 S3 presigned URL을 생성합니다.
    인증 필요.
    """
    # 파일 크기, 타입 등 검증 (실제 앱에서는 더 엄격하게)
    if request.file_size > 100 * 1024 * 1024:  # 100MB 제한
        raise HTTPException(status_code=400, detail="파일 크기가 너무 큽니다 (최대 100MB)")
    
    upload_id = str(uuid.uuid4())
    
    # S3 presigned URL 생성
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    
    try:
        # S3에 저장될 경로
        object_name = f"uploads/{current_user['user_id']}/{upload_id}/{request.filename}"
        
        presigned_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": settings.S3_BUCKET_NAME,
                "Key": object_name,
                "ContentType": request.content_type
            },
            ExpiresIn=3600,  # 1시간 유효
        )
        
        # upload_id와 object_name 매핑을 Redis나 임시 DB 테이블에 저장 가능
        
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Presigned URL 생성 실패: {e}")

    return {"upload_id": upload_id, "presigned_url": presigned_url}


@router.post("/upload/finalize", response_model=schemas.Track)
async def finalize_upload(
    request: schemas.UploadFinalizeRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    음악 업로드를 완료하고 DB에 트랙을 생성합니다.
    인증 필요.
    """
    # S3에 업로드된 파일 URL 구성
    file_url = f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/uploads/{current_user['user_id']}/{request.upload_id}/{request.title}"
    
    # 현재 사용자의 DB 프로필에서 닉네임 가져오기
    db_user = current_user["db_user"]
    
    track_create = schemas.TrackCreate(
        title=request.title,
        artist_name=db_user.nickname,
        description=request.description,
        cover_image_url=request.cover_image_url,
        file_url=file_url
    )
    
    # 트랙 생성 (owner_id는 현재 사용자의 DB ID)
    return crud.create_track(db=db, track=track_create, owner_id=current_user["db_user_id"])


@router.get("/{track_id}", response_model=schemas.Track)
def read_track(track_id: int, db: Session = Depends(get_db)):
    """
    트랙 정보를 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    db_track = crud.get_track(db, track_id=track_id)
    if db_track is None:
        raise HTTPException(status_code=404, detail="트랙을 찾을 수 없습니다")
    return db_track


@router.post("/upload/local", response_model=schemas.Track)
async def upload_track_local(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist_name: str = Form(...),
    description: str = Form(None),
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    로컬 파일 업로드 (테스트용).
    파일을 로컬 디렉토리에 저장하고 트랙을 생성합니다.
    인증 필요.
    """
    # 파일 타입 검증
    allowed_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg"]
    if file.content_type not in allowed_types:
        raise ValidationError(f"지원하지 않는 파일 형식입니다. 허용: {', '.join(allowed_types)}")
    
    # 파일 크기 검증 (50MB 제한)
    max_size = 50 * 1024 * 1024  # 50MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise ValidationError("파일 크기는 50MB를 초과할 수 없습니다")
    
    # 업로드 디렉토리 생성
    upload_dir = Path("uploads/tracks")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 고유한 파일명 생성
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # 파일 저장
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # 파일 URL (로컬 경로)
    file_url = f"/uploads/tracks/{unique_filename}"
    
    # 트랙 생성
    track_data = schemas.TrackCreate(
        title=title,
        artist_name=artist_name,
        file_url=file_url,
        description=description
    )
    
    db_track = crud.create_track(db, track=track_data, owner_id=current_user["db_user_id"])
    
    return db_track


@router.post("/upload/test", response_model=schemas.Track)
async def upload_track_test(
    file: UploadFile = File(...),
    title: str = Form(...),
    artist_name: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    """
    테스트용 파일 업로드 (인증 불필요).
    개발/테스트 환경에서만 사용하세요!
    """
    # 파일 타입 검증
    allowed_types = ["audio/mpeg", "audio/mp3", "audio/wav", "audio/ogg", "audio/x-m4a"]
    if file.content_type not in allowed_types:
        raise ValidationError(f"지원하지 않는 파일 형식입니다. 허용: {', '.join(allowed_types)}")
    
    # 파일 크기 검증 (50MB 제한)
    max_size = 50 * 1024 * 1024  # 50MB
    file_content = await file.read()
    if len(file_content) > max_size:
        raise ValidationError("파일 크기는 50MB를 초과할 수 없습니다")
    
    # 업로드 디렉토리 생성
    upload_dir = Path("uploads/tracks")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 고유한 파일명 생성
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = upload_dir / unique_filename
    
    # 파일 저장
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # 파일 URL (로컬 경로)
    file_url = f"/uploads/tracks/{unique_filename}"
    
    # 테스트용 사용자 생성 또는 가져오기
    test_user = crud.get_user_profile_by_user_id(db, "test_user")
    if not test_user:
        test_user_data = schemas.UserProfileCreate(
            user_id="test_user",
            nickname="테스트 사용자"
        )
        test_user = crud.create_user_profile(db, test_user_data)
    
    # 트랙 생성
    track_data = schemas.TrackCreate(
        title=title,
        artist_name=artist_name,
        file_url=file_url,
        description=description
    )
    
    db_track = crud.create_track(db, track=track_data, owner_id=test_user.id)
    
    return db_track


@router.get("/", response_model=List[schemas.Track])
def read_tracks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    트랙 목록을 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    tracks = crud.get_tracks(db, skip=skip, limit=limit)
    return tracks


@router.get("/{track_id}/stream")
async def stream_track(
    track_id: int,
    current_user: dict = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    트랙을 스트리밍합니다 (Proxy Streaming).
    파일 경로를 숨기고 안전하게 제공합니다.
    공개 엔드포인트이지만, 인증된 사용자는 재생 기록이 저장됩니다.
    """
    # 트랙 조회
    track = crud.get_track(db, track_id=track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    # 파일 경로 확인
    # file_url이 "/uploads/tracks/xxx.mp3" 형식이므로 앞의 "/" 제거
    file_path = Path(track.file_url.lstrip("/"))
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="파일을 찾을 수 없습니다")
    
    # 인증된 사용자의 경우 재생 기록 저장
    if current_user:
        try:
            crud.create_play_history(db, user_id=current_user["db_user_id"], track_id=track_id)
        except Exception as e:
            # 재생 기록 저장 실패해도 스트리밍은 계속
            print(f"재생 기록 저장 실패: {e}")
    
    # 파일 타입에 따른 MIME type 설정
    mime_types = {
        ".mp3": "audio/mpeg",
        ".wav": "audio/wav",
        ".ogg": "audio/ogg",
        ".m4a": "audio/mp4"
    }
    media_type = mime_types.get(file_path.suffix.lower(), "audio/mpeg")
    
    # 파일 스트리밍 (Range 요청 지원)
    return FileResponse(
        path=str(file_path),
        media_type=media_type,
        filename=f"{track.title}{file_path.suffix}"
    )
