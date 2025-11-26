from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import schemas
from app.crud import crud
from app.db.database import get_db
from app.api.dependencies import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=schemas.UserProfile)
async def read_current_user(
    current_user: dict = Depends(get_current_active_user)
):
    """
    현재 로그인한 사용자의 프로필을 조회합니다.
    인증 필요.
    """
    return current_user["db_user"]


@router.patch("/me", response_model=schemas.UserProfile)
async def update_current_user(
    user_update: schemas.UserProfileUpdate,
    current_user: dict = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    현재 로그인한 사용자의 프로필을 수정합니다.
    인증 필요.
    """
    db_user = current_user["db_user"]
    
    # 업데이트할 필드만 적용
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.get("/{user_id}", response_model=schemas.UserProfile)
def read_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    특정 사용자의 프로필을 조회합니다.
    공개 엔드포인트 (인증 불필요).
    """
    db_user = crud.get_user_profile(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다")
    return db_user


@router.post("/", response_model=schemas.UserProfile)
def create_user_profile(user: schemas.UserProfileCreate, db: Session = Depends(get_db)):
    """
    사용자 프로필을 생성합니다.
    (주의: 실제로는 JWT 검증 시 자동 생성되므로 이 엔드포인트는 테스트/관리용)
    """
    db_user = crud.get_user_profile_by_user_id(db, user_id=user.user_id)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 사용자입니다")
    return crud.create_user_profile(db=db, user=user)
