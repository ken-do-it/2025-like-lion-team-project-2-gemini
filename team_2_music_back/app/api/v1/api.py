from fastapi import APIRouter
from app.api.v1.endpoints import users, tracks, likes, comments, follows, playlists, play_history

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tracks.router, prefix="/tracks", tags=["tracks"])
api_router.include_router(likes.router, tags=["likes"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(follows.router, prefix="/follows", tags=["follows"])
api_router.include_router(playlists.router, prefix="/playlists", tags=["playlists"])
api_router.include_router(play_history.router, tags=["play-history"])
