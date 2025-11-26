from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.models import TrackStatus

# Base Schemas
class UserProfileBase(BaseModel):
    nickname: Optional[str] = None
    profile_image_url: Optional[str] = None
    bio: Optional[str] = None

class UserProfileCreate(UserProfileBase):
    user_id: str # From Auth Server
    nickname: str

class UserProfileUpdate(UserProfileBase):
    pass

class UserProfile(UserProfileBase):
    id: int
    user_id: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TrackBase(BaseModel):
    title: str
    description: Optional[str] = None
    cover_image_url: Optional[str] = None

class TrackCreate(TrackBase):
    artist_name: str
    file_url: str

class TrackUpdate(TrackBase):
    pass

class Track(TrackBase):
    id: int
    artist_name: str
    file_url: str
    duration: Optional[float] = None
    status: TrackStatus
    trending_score: float
    owner_user_id: int
    created_at: datetime
    owner: UserProfile

    class Config:
        from_attributes = True


class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    track_id: int

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    track_id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user: UserProfile

    class Config:
        from_attributes = True


class LikeBase(BaseModel):
    track_id: int

class LikeCreate(LikeBase):
    pass

class Like(LikeBase):
    user_id: int
    created_at: datetime
    user: UserProfile

    class Config:
        from_attributes = True


# 좋아요 응답 스키마
class LikeResponse(BaseModel):
    message: str
    like_count: int
    is_liked: bool = True


class LikeListResponse(BaseModel):
    likes: List[Like]
    total: int


# 댓글 응답 스키마
class CommentListResponse(BaseModel):
    comments: List[Comment]
    total: int


# 팔로우 스키마
class Follow(BaseModel):
    follower_id: int
    following_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FollowResponse(BaseModel):
    message: str
    follower_count: int
    following_count: int
    is_following: bool = True


class FollowListResponse(BaseModel):
    users: List[UserProfile]
    total: int


class PlaylistBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_public: bool = True

class PlaylistCreate(PlaylistBase):
    pass

class PlaylistUpdate(PlaylistBase):
    pass

class Playlist(PlaylistBase):
    id: int
    owner_user_id: int
    created_at: datetime
    owner: UserProfile

    class Config:
        from_attributes = True


class PlaylistWithTracks(Playlist):
    """트랙 목록을 포함한 플레이리스트"""
    tracks: List[Track] = []


class AddTrackRequest(BaseModel):
    """플레이리스트에 트랙 추가 요청"""
    track_id: int


class AddTrackResponse(BaseModel):
    """트랙 추가 응답"""
    message: str
    playlist_id: int
    track_count: int


class ReorderTrackRequest(BaseModel):
    """트랙 순서 변경 요청"""
    track_id: int
    new_order: int


# 재생 기록 스키마
class PlayHistory(BaseModel):
    id: int
    user_id: int
    track_id: int
    played_at: datetime
    track: Track

    class Config:
        from_attributes = True


class PlayHistoryResponse(BaseModel):
    message: str
    track_id: int

# Schemas for Music Upload Flow
class UploadInitiateRequest(BaseModel):
    filename: str
    content_type: str
    file_size: int

class UploadInitiateResponse(BaseModel):
    upload_id: str
    presigned_url: str

class UploadFinalizeRequest(BaseModel):
    upload_id: str
    title: str
    tags: Optional[List[str]] = []
    description: Optional[str] = None
    cover_image_url: Optional[str] = None

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

