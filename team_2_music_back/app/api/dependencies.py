from fastapi import Depends, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session

from app.core.jwt_utils import verify_token, extract_user_info
from app.core.exceptions import AuthenticationError
from app.db.database import get_db
from app.crud import crud
from app.schemas import schemas

# HTTP Bearer 토큰 스키마
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, Any]:
    """
    JWT 토큰을 검증하고 현재 사용자 정보를 반환합니다.
    
    Args:
        credentials: HTTP Authorization 헤더의 Bearer 토큰
        
    Returns:
        사용자 정보 딕셔너리 (user_id, email, roles, nickname)
        
    Raises:
        AuthenticationError: 토큰이 유효하지 않은 경우
    """
    token = credentials.credentials
    
    # 개발용 토큰 확인
    if token == "dev-token-2025":
        return {
            "user_id": "dev_user_1",
            "email": "dev@example.com",
            "nickname": "Developer",
            "roles": ["admin"]
        }
    
    # JWT 검증
    payload = await verify_token(token)
    
    # 사용자 정보 추출
    user_info = extract_user_info(payload)
    
    if not user_info.get("user_id"):
        raise AuthenticationError(
            message="토큰에서 사용자 ID를 찾을 수 없습니다",
            details={"error": "Missing 'sub' claim in token"}
        )
    
    return user_info


async def get_current_active_user(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    현재 사용자가 활성 상태인지 확인합니다.
    데이터베이스에 사용자 프로필이 없으면 자동으로 생성합니다.
    
    Args:
        current_user: JWT에서 추출한 사용자 정보
        db: 데이터베이스 세션
        
    Returns:
        사용자 정보 딕셔너리 (DB 프로필 포함)
        
    Raises:
        AuthenticationError: 사용자가 비활성 상태인 경우
    """
    user_id = current_user["user_id"]
    
    # DB에서 사용자 프로필 조회
    db_user = crud.get_user_profile_by_user_id(db, user_id=user_id)
    
    # 프로필이 없으면 자동 생성
    if not db_user:
        user_profile_create = schemas.UserProfileCreate(
            user_id=user_id,
            nickname=current_user.get("nickname") or current_user.get("email", "").split("@")[0],
            bio=None,
            profile_image_url=None
        )
        db_user = crud.create_user_profile(db, user=user_profile_create)
    
    # 비활성 사용자 체크
    if not db_user.is_active:
        raise AuthenticationError(
            message="비활성화된 계정입니다",
            details={"user_id": user_id}
        )
    
    # 사용자 정보에 DB ID 추가
    current_user["db_user_id"] = db_user.id
    current_user["db_user"] = db_user
    
    return current_user


async def get_optional_user(
    authorization: Optional[str] = Header(None)
) -> Optional[Dict[str, Any]]:
    """
    선택적 인증 - 토큰이 있으면 검증하고, 없으면 None 반환
    공개 엔드포인트에서 사용 (로그인 여부에 따라 다른 응답)
    
    Args:
        authorization: Authorization 헤더 (선택사항)
        
    Returns:
        사용자 정보 또는 None
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None
    
    token = authorization.replace("Bearer ", "")
    
    # 개발용 토큰 확인
    if token == "dev-token-2025":
        return {
            "user_id": "dev_user_1",
            "email": "dev@example.com",
            "nickname": "Developer",
            "roles": ["admin"]
        }
    
    try:
        payload = await verify_token(token)
        user_info = extract_user_info(payload)
        return user_info
    except AuthenticationError:
        # 토큰이 유효하지 않아도 None 반환 (공개 엔드포인트이므로)
        return None
