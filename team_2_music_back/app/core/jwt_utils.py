import httpx
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError, JWTClaimsError
from typing import Dict, Any, Optional
from app.core.config import settings
from app.core.redis_client import cache_get, cache_set
from app.core.exceptions import AuthenticationError

# 캐시 키
JWKS_CACHE_KEY = "jwks:cache"


async def get_jwks() -> Dict[str, Any]:
    """
    권한 서버에서 JWKS(JSON Web Key Set)를 가져옵니다.
    Redis에 캐싱되어 있으면 캐시에서 반환하고, 없으면 서버에서 가져와 캐싱합니다.
    
    Returns:
        JWKS 딕셔너리
        
    Raises:
        AuthenticationError: JWKS를 가져오는데 실패한 경우
    """
    # 캐시 확인
    cached_jwks = cache_get(JWKS_CACHE_KEY)
    if cached_jwks:
        return cached_jwks
    
    # 권한 서버에서 JWKS 가져오기
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                settings.AUTH_SERVER_JWKS_URL,
                timeout=10.0
            )
            response.raise_for_status()
            jwks = response.json()
            
            # Redis에 캐싱 (1시간)
            cache_set(JWKS_CACHE_KEY, jwks, ttl=settings.REDIS_CACHE_TTL_JWKS)
            
            return jwks
    except httpx.HTTPError as e:
        raise AuthenticationError(
            message="JWKS를 가져오는데 실패했습니다",
            details={"error": str(e)}
        )


def get_public_key_from_jwks(token: str, jwks: Dict[str, Any]) -> Optional[str]:
    """
    JWT 토큰의 헤더에서 kid를 추출하고, JWKS에서 해당하는 공개키를 찾습니다.
    
    Args:
        token: JWT 토큰
        jwks: JWKS 딕셔너리
        
    Returns:
        공개키 (PEM 형식) 또는 None
    """
    try:
        # 토큰 헤더 디코딩 (검증 없이)
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        
        if not kid:
            return None
        
        # JWKS에서 kid에 해당하는 키 찾기
        for key in jwks.get("keys", []):
            if key.get("kid") == kid:
                # JWK를 PEM 형식으로 변환하여 반환
                # python-jose는 JWK 딕셔너리를 직접 사용할 수 있음
                return key
        
        return None
    except JWTError:
        return None


async def verify_token(token: str) -> Dict[str, Any]:
    """
    JWT 토큰을 검증하고 페이로드를 반환합니다.
    
    Args:
        token: JWT 토큰 문자열
        
    Returns:
        디코딩된 토큰 페이로드 (user_id, email, roles 등)
        
    Raises:
        AuthenticationError: 토큰이 유효하지 않은 경우
    """
    try:
        # JWKS 가져오기
        jwks = await get_jwks()
        
        # 공개키 찾기
        public_key = get_public_key_from_jwks(token, jwks)
        if not public_key:
            raise AuthenticationError(
                message="토큰의 서명 키를 찾을 수 없습니다",
                details={"error": "Invalid kid in token header"}
            )
        
        # JWT 검증 및 디코딩
        payload = jwt.decode(
            token,
            public_key,
            algorithms=[settings.JWT_ALGORITHM],
            audience=settings.JWT_AUDIENCE if settings.JWT_AUDIENCE else None,
            issuer=settings.JWT_ISSUER if settings.JWT_ISSUER else None,
        )
        
        return payload
        
    except ExpiredSignatureError:
        raise AuthenticationError(
            message="토큰이 만료되었습니다",
            details={"error": "Token expired"}
        )
    except JWTClaimsError as e:
        raise AuthenticationError(
            message="토큰 클레임이 유효하지 않습니다",
            details={"error": str(e)}
        )
    except JWTError as e:
        raise AuthenticationError(
            message="토큰이 유효하지 않습니다",
            details={"error": str(e)}
        )


def extract_user_info(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    JWT 페이로드에서 사용자 정보를 추출합니다.
    
    Args:
        payload: JWT 페이로드
        
    Returns:
        사용자 정보 딕셔너리
    """
    return {
        "user_id": payload.get("sub"),  # subject (사용자 ID)
        "email": payload.get("email"),
        "roles": payload.get("roles", []),
        "nickname": payload.get("nickname") or payload.get("name"),
    }
