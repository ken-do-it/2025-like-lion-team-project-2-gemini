from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.api.dependencies import get_current_active_user
from app.core.exceptions import ResourceNotFoundError

router = APIRouter()


@router.post("/tracks/{track_id}/play", response_model=schemas.PlayHistoryResponse)
async def record_play(
    track_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    트랙 재생을 기록합니다.
    인증 필요.
    """
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    # 재생 기록 생성
    crud.create_play_history(db, user_id=current_user["db_user_id"], track_id=track_id)
    
    return {
        "message": "재생 기록이 저장되었습니다",
        "track_id": track_id
    }


@router.get("/users/me/history", response_model=List[schemas.PlayHistory])
async def get_my_play_history(
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    내 재생 기록을 조회합니다 (최신순).
    인증 필요.
    """
    history = crud.get_user_play_history(
        db, 
        user_id=current_user["db_user_id"], 
        skip=skip, 
        limit=limit
    )
    return history


@router.get("/users/me/recently-played", response_model=List[schemas.Track])
async def get_recently_played(
    limit: int = 20,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    최근 재생한 트랙 목록을 조회합니다 (중복 제거).
    인증 필요.
    """
    tracks = crud.get_recently_played_tracks(
        db, 
        user_id=current_user["db_user_id"], 
        limit=limit
    )
    return tracks


@router.get("/tracks/{track_id}/play-count")
def get_track_play_count(
    track_id: int,
    db: Session = Depends(get_db)
):
    """
    트랙의 총 재생 수를 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    play_count = crud.get_play_count(db, track_id=track_id)
    
    return {
        "track_id": track_id,
        "play_count": play_count
    }
