from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.api.dependencies import get_current_active_user, get_optional_user
from app.core.exceptions import ResourceNotFoundError, AuthorizationError, DuplicateResourceError

router = APIRouter()


@router.post("/", response_model=schemas.PlaylistWithTracks)
async def create_playlist(
    playlist: schemas.PlaylistCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트를 생성합니다.
    인증 필요.
    """
    db_playlist = crud.create_playlist(db, playlist=playlist, owner_id=current_user["db_user_id"])
    return db_playlist


@router.get("/{playlist_id}", response_model=schemas.PlaylistWithTracks)
async def get_playlist(
    playlist_id: int,
    current_user: dict = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트를 조회합니다.
    공개 플레이리스트는 누구나 조회 가능, 비공개는 소유자만 가능.
    """
    db_playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not db_playlist:
        raise ResourceNotFoundError("플레이리스트")
    
    # 비공개 플레이리스트는 소유자만 조회 가능
    if not db_playlist.is_public:
        if not current_user or db_playlist.owner_user_id != current_user.get("db_user_id"):
            raise AuthorizationError("비공개 플레이리스트는 소유자만 조회할 수 있습니다")
    
    # 트랙 목록 추가
    tracks = crud.get_playlist_tracks(db, playlist_id=playlist_id)
    
    # Pydantic 모델로 변환
    playlist_dict = {
        "id": db_playlist.id,
        "name": db_playlist.name,
        "description": db_playlist.description,
        "is_public": db_playlist.is_public,
        "owner_user_id": db_playlist.owner_user_id,
        "created_at": db_playlist.created_at,
        "owner": db_playlist.owner,
        "tracks": tracks
    }
    
    return playlist_dict


@router.patch("/{playlist_id}", response_model=schemas.Playlist)
async def update_playlist(
    playlist_id: int,
    playlist_update: schemas.PlaylistUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트를 수정합니다.
    인증 필요 (소유자만 가능).
    """
    db_playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not db_playlist:
        raise ResourceNotFoundError("플레이리스트")
    
    # 소유자 확인
    if db_playlist.owner_user_id != current_user["db_user_id"]:
        raise AuthorizationError("플레이리스트 소유자만 수정할 수 있습니다")
    
    # 업데이트
    update_data = playlist_update.dict(exclude_unset=True)
    updated_playlist = crud.update_playlist(db, playlist=db_playlist, update_data=update_data)
    
    return updated_playlist


@router.delete("/{playlist_id}")
async def delete_playlist(
    playlist_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트를 삭제합니다.
    인증 필요 (소유자만 가능).
    """
    db_playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not db_playlist:
        raise ResourceNotFoundError("플레이리스트")
    
    # 소유자 확인
    if db_playlist.owner_user_id != current_user["db_user_id"]:
        raise AuthorizationError("플레이리스트 소유자만 삭제할 수 있습니다")
    
    crud.delete_playlist(db, playlist=db_playlist)
    
    return {"message": "플레이리스트가 삭제되었습니다"}


@router.get("/users/{user_id}/playlists", response_model=List[schemas.Playlist])
def get_user_playlists(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    current_user: dict = Depends(get_optional_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 플레이리스트 목록을 조회합니다.
    공개 플레이리스트는 누구나, 비공개는 본인만 조회 가능.
    """
    # 사용자 존재 확인
    user = crud.get_user_profile(db, user_id=user_id)
    if not user:
        raise ResourceNotFoundError("사용자")
    
    playlists = crud.get_user_playlists(db, user_id=user_id, skip=skip, limit=limit)
    
    # 본인이 아니면 공개 플레이리스트만 필터링
    if not current_user or current_user.get("db_user_id") != user_id:
        playlists = [p for p in playlists if p.is_public]
    
    return playlists


@router.post("/{playlist_id}/tracks", response_model=schemas.AddTrackResponse)
async def add_track_to_playlist(
    playlist_id: int,
    request: schemas.AddTrackRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트에 트랙을 추가합니다.
    인증 필요 (소유자만 가능).
    """
    # 플레이리스트 존재 확인
    db_playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not db_playlist:
        raise ResourceNotFoundError("플레이리스트")
    
    # 소유자 확인
    if db_playlist.owner_user_id != current_user["db_user_id"]:
        raise AuthorizationError("플레이리스트 소유자만 트랙을 추가할 수 있습니다")
    
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=request.track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    # 트랙 추가
    try:
        crud.add_track_to_playlist(db, playlist_id=playlist_id, track_id=request.track_id)
    except IntegrityError:
        db.rollback()
        raise DuplicateResourceError("플레이리스트에 이미 존재하는 트랙")
    
    track_count = crud.get_playlist_track_count(db, playlist_id=playlist_id)
    
    return {
        "message": "트랙이 추가되었습니다",
        "playlist_id": playlist_id,
        "track_count": track_count
    }


@router.delete("/{playlist_id}/tracks/{track_id}")
async def remove_track_from_playlist(
    playlist_id: int,
    track_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트에서 트랙을 삭제합니다.
    인증 필요 (소유자만 가능).
    """
    # 플레이리스트 존재 확인
    db_playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not db_playlist:
        raise ResourceNotFoundError("플레이리스트")
    
    # 소유자 확인
    if db_playlist.owner_user_id != current_user["db_user_id"]:
        raise AuthorizationError("플레이리스트 소유자만 트랙을 삭제할 수 있습니다")
    
    # 트랙 삭제
    deleted = crud.remove_track_from_playlist(db, playlist_id=playlist_id, track_id=track_id)
    if not deleted:
        raise ResourceNotFoundError("플레이리스트에서 트랙")
    
    return {"message": "트랙이 삭제되었습니다"}


@router.patch("/{playlist_id}/tracks/reorder")
async def reorder_playlist_tracks(
    playlist_id: int,
    request: schemas.ReorderTrackRequest,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    플레이리스트 트랙의 순서를 변경합니다.
    인증 필요 (소유자만 가능).
    """
    # 플레이리스트 존재 확인
    db_playlist = crud.get_playlist(db, playlist_id=playlist_id)
    if not db_playlist:
        raise ResourceNotFoundError("플레이리스트")
    
    # 소유자 확인
    if db_playlist.owner_user_id != current_user["db_user_id"]:
        raise AuthorizationError("플레이리스트 소유자만 순서를 변경할 수 있습니다")
    
    # 순서 변경
    success = crud.reorder_playlist_track(
        db, 
        playlist_id=playlist_id, 
        track_id=request.track_id, 
        new_order=request.new_order
    )
    
    if not success:
        raise ResourceNotFoundError("플레이리스트에서 트랙")
    
    return {"message": "트랙 순서가 변경되었습니다"}
