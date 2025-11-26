import redis
import json
from typing import Optional, Any
from app.core.config import settings

# Redis 클라이언트 인스턴스
_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> redis.Redis:
    """Redis 클라이언트 인스턴스를 반환합니다."""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
    return _redis_client


def close_redis_client():
    """Redis 연결을 닫습니다."""
    global _redis_client
    if _redis_client is not None:
        _redis_client.close()
        _redis_client = None


def cache_get(key: str) -> Optional[Any]:
    """
    Redis에서 캐시된 값을 가져옵니다.
    
    Args:
        key: 캐시 키
        
    Returns:
        캐시된 값 (JSON 디코딩됨) 또는 None
    """
    try:
        client = get_redis_client()
        value = client.get(key)
        if value:
            return json.loads(value)
        return None
    except (redis.RedisError, json.JSONDecodeError) as e:
        print(f"Redis cache_get error: {e}")
        return None


def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Redis에 값을 캐싱합니다.
    
    Args:
        key: 캐시 키
        value: 캐싱할 값 (JSON 직렬화 가능해야 함)
        ttl: 만료 시간 (초), 기본값 1시간
        
    Returns:
        성공 여부
    """
    try:
        client = get_redis_client()
        serialized_value = json.dumps(value)
        client.setex(key, ttl, serialized_value)
        return True
    except (redis.RedisError, TypeError) as e:
        print(f"Redis cache_set error: {e}")
        return False


def cache_delete(key: str) -> bool:
    """
    Redis에서 캐시를 삭제합니다.
    
    Args:
        key: 삭제할 캐시 키
        
    Returns:
        성공 여부
    """
    try:
        client = get_redis_client()
        client.delete(key)
        return True
    except redis.RedisError as e:
        print(f"Redis cache_delete error: {e}")
        return False
