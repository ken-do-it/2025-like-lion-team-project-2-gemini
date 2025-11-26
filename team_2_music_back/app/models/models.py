from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Boolean,
    ForeignKey,
    Text,
    Enum,
    Float,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.db.database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)  # From Auth Server
    nickname = Column(String, index=True)
    profile_image_url = Column(String)
    bio = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tracks = relationship("Track", back_populates="owner")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")
    playlists = relationship("Playlist", back_populates="owner")
    play_history = relationship("PlayHistory", back_populates="user")

    # For following system
    following = relationship(
        "Follow",
        foreign_keys="[Follow.follower_id]",
        back_populates="follower",
        cascade="all, delete-orphan",
    )
    followers = relationship(
        "Follow",
        foreign_keys="[Follow.following_id]",
        back_populates="following",
        cascade="all, delete-orphan",
    )


class Follow(Base):
    __tablename__ = "follows"
    follower_id = Column(Integer, ForeignKey("user_profiles.id"), primary_key=True)
    following_id = Column(Integer, ForeignKey("user_profiles.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    follower = relationship("UserProfile", foreign_keys=[follower_id], back_populates="following")
    following = relationship("UserProfile", foreign_keys=[following_id], back_populates="followers")


class TrackStatus(enum.Enum):
    processing = "processing"
    ready = "ready"
    failed = "failed"


class Track(Base):
    __tablename__ = "tracks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    artist_name = Column(String, index=True) # Should be linked to UserProfile nickname
    description = Column(Text)
    file_url = Column(String, nullable=False)
    cover_image_url = Column(String)
    duration = Column(Float) # in seconds
    status = Column(Enum(TrackStatus), default=TrackStatus.processing)
    trending_score = Column(Float, default=0.0, index=True)
    
    owner_user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    owner = relationship("UserProfile", back_populates="tracks")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    comments = relationship("Comment", back_populates="track", cascade="all, delete-orphan")
    likes = relationship("Like", back_populates="track", cascade="all, delete-orphan")
    tags = relationship("TrackTag", back_populates="track", cascade="all, delete-orphan")


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)

    tracks = relationship("TrackTag", back_populates="tag")


class TrackTag(Base):
    __tablename__ = "track_tags"
    track_id = Column(Integer, ForeignKey("tracks.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    track = relationship("Track", back_populates="tags")
    tag = relationship("Tag", back_populates="tracks")


class Like(Base):
    __tablename__ = "likes"
    track_id = Column(Integer, ForeignKey("tracks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    track = relationship("Track", back_populates="likes")
    user = relationship("UserProfile", back_populates="likes")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    track = relationship("Track", back_populates="comments")
    user = relationship("UserProfile", back_populates="comments")


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    is_public = Column(Boolean, default=True)

    owner_user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False)
    owner = relationship("UserProfile", back_populates="playlists")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    tracks = relationship("PlaylistTrack", back_populates="playlist", cascade="all, delete-orphan")


class PlaylistTrack(Base):
    __tablename__ = "playlist_tracks"
    playlist_id = Column(Integer, ForeignKey("playlists.id"), primary_key=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), primary_key=True)
    track_order = Column(Integer)

    playlist = relationship("Playlist", back_populates="tracks")
    track = relationship("Track")


class PlayHistory(Base):
    __tablename__ = "play_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_profiles.id"), nullable=False, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"), nullable=False)
    played_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    user = relationship("UserProfile", back_populates="play_history")
    track = relationship("Track")
