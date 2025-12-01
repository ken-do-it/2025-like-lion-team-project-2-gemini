from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.api.dependencies import get_current_active_user, get_optional_user
from app.core.exceptions import DuplicateResourceError, ResourceNotFoundError

router = APIRouter()


@router.post("/", response_model=schemas.LikeResponse)
async def toggle_like(
    like_in: schemas.LikeCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    좋아요를 토글합니다 (있으면 삭제, 없으면 추가).
    인증 필요.
    """
    track_id = like_in.track_id
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    # 이미 좋아요했는지 확인
    existing_like = crud.get_like(db, track_id=track_id, user_id=current_user["db_user_id"])
    
    if existing_like:
        # 있으면 삭제 (취소)
        crud.delete_like(db, track_id=track_id, user_id=current_user["db_user_id"])
        is_liked = False
        message = "좋아요를 취소했습니다"
    else:
        # 없으면 추가
        try:
            crud.create_like(db, track_id=track_id, user_id=current_user["db_user_id"])
            is_liked = True
            message = "좋아요를 추가했습니다"
        except IntegrityError:
            db.rollback()
            raise DuplicateResourceError("좋아요")
    
    # 좋아요 수 조회
    like_count = crud.get_track_like_count(db, track_id=track_id)
    
    return {
        "message": message,
        "like_count": like_count,
        "is_liked": is_liked
    }


@router.get("/track/{track_id}", response_model=schemas.LikeListResponse)
def get_track_likes(
    track_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    트랙의 좋아요 목록을 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    likes = crud.get_track_likes(db, track_id=track_id, skip=skip, limit=limit)
    total = crud.get_track_like_count(db, track_id=track_id)
    
    return {
        "likes": likes,
        "total": total
    }


@router.get("/users/me/likes", response_model=List[schemas.Track])
async def get_my_liked_tracks(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    내가 좋아요한 트랙 목록을 조회합니다.
    인증 필요.
    """
    likes = crud.get_user_likes(db, user_id=current_user["db_user_id"], skip=skip, limit=limit)
    
    # 좋아요한 트랙들 반환
    tracks = [crud.get_track(db, like.track_id) for like in likes]
    return [track for track in tracks if track is not None]
