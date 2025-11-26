from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.api.dependencies import get_current_active_user
from app.core.exceptions import ResourceNotFoundError, AuthorizationError

router = APIRouter()


@router.post("/", response_model=schemas.Comment)
async def create_comment(
    comment: schemas.CommentCreate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    댓글을 작성합니다.
    인증 필요.
    """
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=comment.track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    # 댓글 작성
    db_comment = crud.create_comment(db, comment=comment, user_id=current_user["db_user_id"])
    
    return db_comment


@router.get("/tracks/{track_id}/comments", response_model=schemas.CommentListResponse)
def get_track_comments(
    track_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    트랙의 댓글 목록을 조회합니다 (최신순).
    공개 엔드포인트 (인증 불필요).
    """
    # 트랙 존재 확인
    track = crud.get_track(db, track_id=track_id)
    if not track:
        raise ResourceNotFoundError("트랙")
    
    comments = crud.get_track_comments(db, track_id=track_id, skip=skip, limit=limit)
    total = crud.get_track_comment_count(db, track_id=track_id)
    
    return {
        "comments": comments,
        "total": total
    }


@router.get("/{comment_id}", response_model=schemas.Comment)
def get_comment(
    comment_id: int,
    db: Session = Depends(get_db)
):
    """
    댓글 상세를 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    comment = crud.get_comment(db, comment_id=comment_id)
    if not comment:
        raise ResourceNotFoundError("댓글")
    
    return comment


@router.patch("/{comment_id}", response_model=schemas.Comment)
async def update_comment(
    comment_id: int,
    comment_update: schemas.CommentUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    댓글을 수정합니다.
    인증 필요 (작성자만 가능).
    """
    # 댓글 존재 확인
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise ResourceNotFoundError("댓글")
    
    # 권한 확인 (작성자만 수정 가능)
    if db_comment.user_id != current_user["db_user_id"]:
        raise AuthorizationError("댓글 작성자만 수정할 수 있습니다")
    
    # 댓글 수정
    updated_comment = crud.update_comment(db, comment=db_comment, content=comment_update.content)
    
    return updated_comment


@router.delete("/{comment_id}")
async def delete_comment(
    comment_id: int,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    댓글을 삭제합니다.
    인증 필요 (작성자만 가능).
    """
    # 댓글 존재 확인
    db_comment = crud.get_comment(db, comment_id=comment_id)
    if not db_comment:
        raise ResourceNotFoundError("댓글")
    
    # 권한 확인 (작성자만 삭제 가능)
    if db_comment.user_id != current_user["db_user_id"]:
        raise AuthorizationError("댓글 작성자만 삭제할 수 있습니다")
    
    # 댓글 삭제
    crud.delete_comment(db, comment=db_comment)
    
    return {"message": "댓글이 삭제되었습니다"}
