from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import models
from app.schemas import schemas
from typing import List, Optional

# UserProfile CRUD
def get_user_profile(db: Session, user_id: int):
    return db.query(models.UserProfile).filter(models.UserProfile.id == user_id).first()

def get_user_profile_by_user_id(db: Session, user_id: str):
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def create_user_profile(db: Session, user: schemas.UserProfileCreate):
    db_user = models.UserProfile(
        user_id=user.user_id,
        nickname=user.nickname,
        profile_image_url=user.profile_image_url,
        bio=user.bio
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Track CRUD
def get_track(db: Session, track_id: int):
    return db.query(models.Track).filter(models.Track.id == track_id).first()

def get_tracks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Track).offset(skip).limit(limit).all()

def search_tracks(db: Session, query: str, skip: int = 0, limit: int = 100):
    """트랙 검색 (제목, 아티스트, 설명)"""
    search_query = f"%{query}%"
    return db.query(models.Track).filter(
        (models.Track.title.ilike(search_query)) |
        (models.Track.artist_name.ilike(search_query)) |
        (models.Track.description.ilike(search_query))
    ).offset(skip).limit(limit).all()

def create_track(db: Session, track: schemas.TrackCreate, owner_id: int):
    db_track = models.Track(**track.dict(), owner_user_id=owner_id)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track

def update_track(db: Session, track_id: int, track_update: schemas.TrackUpdate):
    """트랙 정보 업데이트"""
    db_track = db.query(models.Track).filter(models.Track.id == track_id).first()
    if not db_track:
        return None
    
    # 업데이트할 필드만 적용
    update_data = track_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_track, field, value)
    
    db.commit()
    db.refresh(db_track)
    return db_track


# Like CRUD
def create_like(db: Session, track_id: int, user_id: int) -> models.Like:
    """좋아요 추가"""
    db_like = models.Like(track_id=track_id, user_id=user_id)
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


def delete_like(db: Session, track_id: int, user_id: int) -> bool:
    """좋아요 삭제"""
    db_like = db.query(models.Like).filter(
        models.Like.track_id == track_id,
        models.Like.user_id == user_id
    ).first()
    
    if db_like:
        db.delete(db_like)
        db.commit()
        return True
    return False


def get_like(db: Session, track_id: int, user_id: int) -> Optional[models.Like]:
    """특정 좋아요 조회"""
    return db.query(models.Like).filter(
        models.Like.track_id == track_id,
        models.Like.user_id == user_id
    ).first()


def get_track_likes(db: Session, track_id: int, skip: int = 0, limit: int = 100) -> List[models.Like]:
    """트랙의 좋아요 목록"""
    return db.query(models.Like).filter(
        models.Like.track_id == track_id
    ).offset(skip).limit(limit).all()


def get_user_likes(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Like]:
    """사용자가 좋아요한 목록"""
    return db.query(models.Like).filter(
        models.Like.user_id == user_id
    ).offset(skip).limit(limit).all()


def get_track_like_count(db: Session, track_id: int) -> int:
    """트랙의 총 좋아요 수"""
    return db.query(models.Like).filter(models.Like.track_id == track_id).count()


# Comment CRUD
def create_comment(db: Session, comment: schemas.CommentCreate, user_id: int) -> models.Comment:
    """댓글 작성"""
    db_comment = models.Comment(
        content=comment.content,
        track_id=comment.track_id,
        user_id=user_id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def get_comment(db: Session, comment_id: int) -> Optional[models.Comment]:
    """댓글 조회"""
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_track_comments(db: Session, track_id: int, skip: int = 0, limit: int = 100) -> List[models.Comment]:
    """트랙의 댓글 목록 (최신순)"""
    return db.query(models.Comment).filter(
        models.Comment.track_id == track_id
    ).order_by(desc(models.Comment.created_at)).offset(skip).limit(limit).all()


def update_comment(db: Session, comment: models.Comment, content: str) -> models.Comment:
    """댓글 수정"""
    comment.content = content
    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment: models.Comment) -> bool:
    """댓글 삭제"""
    db.delete(comment)
    db.commit()
    return True


def get_track_comment_count(db: Session, track_id: int) -> int:
    """트랙의 총 댓글 수"""
    return db.query(models.Comment).filter(models.Comment.track_id == track_id).count()


# Follow CRUD
def create_follow(db: Session, follower_id: int, following_id: int) -> models.Follow:
    """팔로우 추가"""
    db_follow = models.Follow(follower_id=follower_id, following_id=following_id)
    db.add(db_follow)
    db.commit()
    db.refresh(db_follow)
    return db_follow


def delete_follow(db: Session, follower_id: int, following_id: int) -> bool:
    """언팔로우"""
    db_follow = db.query(models.Follow).filter(
        models.Follow.follower_id == follower_id,
        models.Follow.following_id == following_id
    ).first()
    
    if db_follow:
        db.delete(db_follow)
        db.commit()
        return True
    return False


def get_follow(db: Session, follower_id: int, following_id: int) -> Optional[models.Follow]:
    """팔로우 관계 조회"""
    return db.query(models.Follow).filter(
        models.Follow.follower_id == follower_id,
        models.Follow.following_id == following_id
    ).first()


def get_followers(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.UserProfile]:
    """팔로워 목록 (나를 팔로우하는 사람들)"""
    follows = db.query(models.Follow).filter(
        models.Follow.following_id == user_id
    ).offset(skip).limit(limit).all()
    
    # 팔로워 사용자 프로필 반환
    return [follow.follower for follow in follows]


def get_following(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.UserProfile]:
    """팔로잉 목록 (내가 팔로우하는 사람들)"""
    follows = db.query(models.Follow).filter(
        models.Follow.follower_id == user_id
    ).offset(skip).limit(limit).all()
    
    # 팔로잉 사용자 프로필 반환
    return [follow.following for follow in follows]


def get_follower_count(db: Session, user_id: int) -> int:
    """팔로워 수"""
    return db.query(models.Follow).filter(models.Follow.following_id == user_id).count()


def get_following_count(db: Session, user_id: int) -> int:
    """팔로잉 수"""
    return db.query(models.Follow).filter(models.Follow.follower_id == user_id).count()


# Playlist CRUD
def create_playlist(db: Session, playlist: schemas.PlaylistCreate, owner_id: int) -> models.Playlist:
    """플레이리스트 생성"""
    db_playlist = models.Playlist(
        name=playlist.name,
        description=playlist.description,
        is_public=playlist.is_public,
        owner_user_id=owner_id
    )
    db.add(db_playlist)
    db.commit()
    db.refresh(db_playlist)
    return db_playlist


def get_playlist(db: Session, playlist_id: int) -> Optional[models.Playlist]:
    """플레이리스트 조회"""
    return db.query(models.Playlist).filter(models.Playlist.id == playlist_id).first()


def get_user_playlists(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Playlist]:
    """사용자의 플레이리스트 목록"""
    return db.query(models.Playlist).filter(
        models.Playlist.owner_user_id == user_id
    ).offset(skip).limit(limit).all()


def update_playlist(db: Session, playlist: models.Playlist, update_data: dict) -> models.Playlist:
    """플레이리스트 수정"""
    for field, value in update_data.items():
        setattr(playlist, field, value)
    db.commit()
    db.refresh(playlist)
    return playlist


def delete_playlist(db: Session, playlist: models.Playlist) -> bool:
    """플레이리스트 삭제"""
    db.delete(playlist)
    db.commit()
    return True


def add_track_to_playlist(db: Session, playlist_id: int, track_id: int) -> models.PlaylistTrack:
    """플레이리스트에 트랙 추가"""
    # 현재 플레이리스트의 최대 순서 찾기
    max_order = db.query(func.max(models.PlaylistTrack.track_order)).filter(
        models.PlaylistTrack.playlist_id == playlist_id
    ).scalar()
    
    next_order = (max_order or -1) + 1
    
    db_playlist_track = models.PlaylistTrack(
        playlist_id=playlist_id,
        track_id=track_id,
        track_order=next_order
    )
    db.add(db_playlist_track)
    db.commit()
    db.refresh(db_playlist_track)
    return db_playlist_track


def remove_track_from_playlist(db: Session, playlist_id: int, track_id: int) -> bool:
    """플레이리스트에서 트랙 삭제"""
    db_playlist_track = db.query(models.PlaylistTrack).filter(
        models.PlaylistTrack.playlist_id == playlist_id,
        models.PlaylistTrack.track_id == track_id
    ).first()
    
    if db_playlist_track:
        db.delete(db_playlist_track)
        db.commit()
        return True
    return False


def get_playlist_tracks(db: Session, playlist_id: int) -> List[models.Track]:
    """플레이리스트의 트랙 목록 (순서대로)"""
    playlist_tracks = db.query(models.PlaylistTrack).filter(
        models.PlaylistTrack.playlist_id == playlist_id
    ).order_by(models.PlaylistTrack.track_order).all()
    
    return [pt.track for pt in playlist_tracks]


def get_playlist_track_count(db: Session, playlist_id: int) -> int:
    """플레이리스트의 트랙 수"""
    return db.query(models.PlaylistTrack).filter(
        models.PlaylistTrack.playlist_id == playlist_id
    ).count()


def reorder_playlist_track(db: Session, playlist_id: int, track_id: int, new_order: int) -> bool:
    """플레이리스트 트랙 순서 변경"""
    db_playlist_track = db.query(models.PlaylistTrack).filter(
        models.PlaylistTrack.playlist_id == playlist_id,
        models.PlaylistTrack.track_id == track_id
    ).first()
    
    if db_playlist_track:
        db_playlist_track.track_order = new_order
        db.commit()
        return True
    return False


# PlayHistory CRUD
def create_play_history(db: Session, user_id: int, track_id: int) -> models.PlayHistory:
    """재생 기록 생성"""
    db_play_history = models.PlayHistory(
        user_id=user_id,
        track_id=track_id
    )
    db.add(db_play_history)
    db.commit()
    db.refresh(db_play_history)
    return db_play_history


def get_user_play_history(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.PlayHistory]:
    """사용자의 재생 기록 (최신순)"""
    return db.query(models.PlayHistory).filter(
        models.PlayHistory.user_id == user_id
    ).order_by(desc(models.PlayHistory.played_at)).offset(skip).limit(limit).all()


def get_recently_played_tracks(db: Session, user_id: int, limit: int = 50) -> List[models.Track]:
    """최근 재생한 트랙 목록 (중복 제거)"""
    # 최근 재생 기록에서 트랙 ID만 가져오기 (중복 제거)
    recent_track_ids = db.query(models.PlayHistory.track_id).filter(
        models.PlayHistory.user_id == user_id
    ).order_by(desc(models.PlayHistory.played_at)).distinct().limit(limit).all()
    
    track_ids = [track_id for (track_id,) in recent_track_ids]
    
    # 트랙 정보 가져오기
    if not track_ids:
        return []
    
    tracks = db.query(models.Track).filter(models.Track.id.in_(track_ids)).all()
    
    # 재생 순서대로 정렬
    track_dict = {track.id: track for track in tracks}
    return [track_dict[track_id] for track_id in track_ids if track_id in track_dict]


def get_play_count(db: Session, track_id: int) -> int:
    """트랙의 총 재생 수"""
    return db.query(models.PlayHistory).filter(models.PlayHistory.track_id == track_id).count()

