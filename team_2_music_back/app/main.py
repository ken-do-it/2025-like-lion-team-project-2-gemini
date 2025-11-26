from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.redis_client import get_redis_client, close_redis_client
from app.core.exceptions import (
    MusicAPIException,
    music_api_exception_handler,
    general_exception_handler
)
from app.db.database import Base, engine

# 데이터베이스 테이블 생성 (Alembic 사용 시 주석 처리)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music Sharing API",
    description="음악 공유 SNS 백엔드 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 예외 핸들러 등록
app.add_exception_handler(MusicAPIException, music_api_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)


@app.on_event("startup")
async def startup_event():
    """애플리케이션 시작 시 실행"""
    try:
        # Redis 연결 테스트
        redis_client = get_redis_client()
        redis_client.ping()
        print("✅ Redis 연결 성공")
    except Exception as e:
        print(f"⚠️ Redis 연결 실패: {e}")
        print("Redis 없이 계속 진행합니다 (캐싱 비활성화)")


@app.on_event("shutdown")
async def shutdown_event():
    """애플리케이션 종료 시 실행"""
    close_redis_client()
    print("✅ Redis 연결 종료")


# API 라우터 등록
app.include_router(api_router, prefix=settings.API_V1_STR)

# 업로드 디렉토리 생성
upload_dir = Path("uploads")
upload_dir.mkdir(exist_ok=True)

# 정적 파일 서빙 (업로드된 파일)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "message": "Music Sharing API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
def health_check():
    """헬스 체크 엔드포인트"""
    return {"status": "healthy"}
