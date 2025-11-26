from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Any, Dict, Optional


class MusicAPIException(Exception):
    """기본 커스텀 예외 클래스"""
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class AuthenticationError(MusicAPIException):
    """인증 실패 예외 (401)"""
    def __init__(self, message: str = "인증에 실패했습니다", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="UNAUTHORIZED",
            message=message,
            status_code=401,
            details=details
        )


class AuthorizationError(MusicAPIException):
    """권한 부족 예외 (403)"""
    def __init__(self, message: str = "권한이 부족합니다", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403,
            details=details
        )


class ResourceNotFoundError(MusicAPIException):
    """리소스를 찾을 수 없음 (404)"""
    def __init__(self, resource: str = "리소스", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="NOT_FOUND",
            message=f"{resource}를 찾을 수 없습니다",
            status_code=404,
            details=details
        )


class ValidationError(MusicAPIException):
    """요청 검증 실패 (422)"""
    def __init__(self, message: str = "요청 검증에 실패했습니다", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="VALIDATION_FAILED",
            message=message,
            status_code=422,
            details=details
        )


class DuplicateResourceError(MusicAPIException):
    """중복된 리소스 (409)"""
    def __init__(self, resource: str = "리소스", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="DUPLICATE_RESOURCE",
            message=f"{resource}가 이미 존재합니다",
            status_code=409,
            details=details
        )


class FileUploadError(MusicAPIException):
    """파일 업로드 실패 (500)"""
    def __init__(self, message: str = "파일 업로드에 실패했습니다", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            code="FILE_UPLOAD_FAILED",
            message=message,
            status_code=500,
            details=details
        )


# 예외 핸들러
async def music_api_exception_handler(request: Request, exc: MusicAPIException) -> JSONResponse:
    """커스텀 예외 핸들러"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details
            }
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """일반 예외 핸들러"""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "code": "INTERNAL_SERVER_ERROR",
                "message": "서버 내부 오류가 발생했습니다",
                "details": {}
            }
        }
    )
