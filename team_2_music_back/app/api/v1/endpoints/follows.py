from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.api.dependencies import get_current_active_user
from app.core.exceptions import DuplicateResourceError, ResourceNotFoundError, ValidationError

router = APIRouter()


@router.post("/users/{user_id}/follow", response_model=schemas.FollowResponse)
async def follow_user(
    user_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자를 팔로우합니다.
    인증 필요.
    """
    # 자기 자신 팔로우 방지
    if user_id == current_user["db_user_id"]:
        raise ValidationError("자기 자신을 팔로우할 수 없습니다")
    
    # 팔로우할 사용자 존재 확인
    target_user = crud.get_user_profile(db, user_id=user_id)
    if not target_user:
        raise ResourceNotFoundError("사용자")
    
    # 이미 팔로우했는지 확인
    existing_follow = crud.get_follow(
        db, 
        follower_id=current_user["db_user_id"], 
        following_id=user_id
    )
    if existing_follow:
        raise DuplicateResourceError("팔로우")
    
    # 팔로우 추가
    try:
        crud.create_follow(
            db, 
            follower_id=current_user["db_user_id"], 
            following_id=user_id
        )
    except IntegrityError:
        db.rollback()
        raise DuplicateResourceError("팔로우")
    
    # 팔로워/팔로잉 수 조회
    follower_count = crud.get_follower_count(db, user_id=user_id)
    following_count = crud.get_following_count(db, user_id=current_user["db_user_id"])
    
    return {
        "message": "팔로우했습니다",
        "follower_count": follower_count,
        "following_count": following_count,
        "is_following": True
    }


@router.delete("/users/{user_id}/follow", response_model=schemas.FollowResponse)
async def unfollow_user(
    user_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자를 언팔로우합니다.
    인증 필요.
    """
    # 사용자 존재 확인
    target_user = crud.get_user_profile(db, user_id=user_id)
    if not target_user:
        raise ResourceNotFoundError("사용자")
    
    # 언팔로우
    deleted = crud.delete_follow(
        db, 
        follower_id=current_user["db_user_id"], 
        following_id=user_id
    )
    if not deleted:
        raise ResourceNotFoundError("팔로우")
    
    # 팔로워/팔로잉 수 조회
    follower_count = crud.get_follower_count(db, user_id=user_id)
    following_count = crud.get_following_count(db, user_id=current_user["db_user_id"])
    
    return {
        "message": "언팔로우했습니다",
        "follower_count": follower_count,
        "following_count": following_count,
        "is_following": False
    }


@router.get("/users/{user_id}/followers", response_model=schemas.FollowListResponse)
def get_user_followers(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    사용자의 팔로워 목록을 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    # 사용자 존재 확인
    user = crud.get_user_profile(db, user_id=user_id)
    if not user:
        raise ResourceNotFoundError("사용자")
    
    followers = crud.get_followers(db, user_id=user_id, skip=skip, limit=limit)
    total = crud.get_follower_count(db, user_id=user_id)
    
    return {
        "users": followers,
        "total": total
    }


@router.get("/users/{user_id}/following", response_model=schemas.FollowListResponse)
def get_user_following(
    user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    사용자가 팔로우하는 사람들의 목록을 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    # 사용자 존재 확인
    user = crud.get_user_profile(db, user_id=user_id)
    if not user:
        raise ResourceNotFoundError("사용자")
    
    following = crud.get_following(db, user_id=user_id, skip=skip, limit=limit)
    total = crud.get_following_count(db, user_id=user_id)
    
    return {
        "users": following,
        "total": total
    }


@router.get("/users/{user_id}/follow-status")
async def get_follow_status(
    user_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    현재 사용자와 대상 사용자 간의 팔로우 상태를 확인합니다.
    인증 필요.
    """
    # 사용자 존재 확인
    target_user = crud.get_user_profile(db, user_id=user_id)
    if not target_user:
        raise ResourceNotFoundError("사용자")
    
    # 팔로우 상태 확인
    is_following = crud.get_follow(
        db, 
        follower_id=current_user["db_user_id"], 
        following_id=user_id
    ) is not None
    
    is_followed_by = crud.get_follow(
        db, 
        follower_id=user_id, 
        following_id=current_user["db_user_id"]
    ) is not None
    
    return {
        "is_following": is_following,  # 내가 상대방을 팔로우하는지
        "is_followed_by": is_followed_by,  # 상대방이 나를 팔로우하는지
        "follower_count": crud.get_follower_count(db, user_id=user_id),
        "following_count": crud.get_following_count(db, user_id=user_id)
    }
