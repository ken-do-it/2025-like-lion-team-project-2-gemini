import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_CACHE_TTL_JWKS: int = 3600  # 1시간
    
    # AWS S3
    AWS_ACCESS_KEY_ID: str = os.getenv("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.getenv("AWS_SECRET_ACCESS_KEY", "")
    S3_BUCKET_NAME: str = os.getenv("S3_BUCKET_NAME", "")
    
    # JWT Authentication
    AUTH_SERVER_JWKS_URL: str = os.getenv("AUTH_SERVER_JWKS_URL", "")
    JWT_ALGORITHM: str = "RS256"
    JWT_AUDIENCE: str = os.getenv("JWT_AUDIENCE", "")  # 선택사항
    JWT_ISSUER: str = os.getenv("JWT_ISSUER", "")  # 선택사항
    
    # API
    API_V1_STR: str = "/api/v1"
    
    # CORS
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8080",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ]
    
    class Config:
        case_sensitive = True

settings = Settings()
