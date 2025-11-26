# Music Sharing SNS Backend

음악 공유 소셜 네트워크 서비스를 위한 FastAPI 기반 백엔드 시스템입니다.

## 📚 프로젝트 개요

이 프로젝트는 음악 업로드, 스트리밍, 소셜 인터랙션(좋아요, 댓글, 팔로우) 기능을 제공하는 RESTful API 서버입니다. 마이크로서비스 아키텍처를 지향하며, 인증은 별도의 Auth Server에 위임하고 JWT 검증을 통해 보안을 유지합니다.

### 주요 기능

- **음악 관리**: Presigned URL을 통한 S3 업로드, 트랙 메타데이터 관리
- **소셜 기능**: 사용자 팔로우/언팔로우, 트랙 좋아요, 댓글 작성
- **플레이리스트**: 나만의 플레이리스트 생성 및 관리
- **재생 기록**: 사용자 청취 이력 추적
- **검색 및 탐색**: 태그 기반 검색 (예정)

## 🛠 기술 스택

- **Language**: Python 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **ORM**: SQLAlchemy + Alembic (Migrations)
- **Caching**: Redis 7
- **Storage**: AWS S3
- **Container**: Docker + Docker Compose
- **Server**: Uvicorn (ASGI)

## 🚀 시작하기 (Docker)

가장 쉬운 실행 방법은 Docker Compose를 사용하는 것입니다.

### 사전 요구사항

- Docker Desktop 설치
- AWS S3 버킷 및 자격 증명 (업로드 기능 테스트 시 필요)

### 설치 및 실행

1. **저장소 클론**
   ```bash
   git clone <repository-url>
   cd team_2_music_back
   ```

2. **환경 변수 설정**
   `.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 값을 채웁니다.
   ```bash
   cp .env.example .env
   ```
   
   > **Note**: Docker 실행 시 `DATABASE_URL`과 `REDIS_HOST`는 `compose.yml`에 정의된 값이 우선 적용됩니다.

3. **Docker 컨테이너 실행**
   ```bash
   docker compose up -d
   ```

4. **API 문서 확인**
   브라우저에서 `http://localhost:8000/docs`로 접속하여 Swagger UI를 확인합니다.

## 💻 로컬 개발 환경 설정

Docker 없이 로컬에서 직접 실행하려면 다음 단계를 따르세요.

1. **가상 환경 생성 및 활성화**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

2. **의존성 설치**
   ```bash
   pip install -r requirements.txt
   ```

3. **로컬 서비스 실행 (PostgreSQL, Redis)**
   Docker를 사용하여 DB와 Redis만 실행할 수 있습니다.
   ```bash
   docker run -d --name music-db -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres:15-alpine
   docker run -d --name music-redis -p 6379:6379 redis:7-alpine
   ```

4. **데이터베이스 마이그레이션**
   ```bash
   alembic upgrade head
   ```

5. **서버 실행**
   ```bash
   uvicorn app.main:app --reload
   ```

## 🗄 데이터베이스 마이그레이션

데이터베이스 스키마 변경 사항을 관리하기 위해 Alembic을 사용합니다.

- **새로운 마이그레이션 생성** (모델 변경 후)
  ```bash
  # 로컬
  alembic revision --autogenerate -m "description of changes"
  
  # Docker
  docker compose exec fastapi alembic revision --autogenerate -m "description"
  ```

- **마이그레이션 적용**
  ```bash
  # 로컬
  alembic upgrade head
  
  # Docker
  docker compose exec fastapi alembic upgrade head
  ```

## 📂 프로젝트 구조

```
team_2_music_back/
├── alembic/                # DB 마이그레이션 스크립트
├── app/
│   ├── api/                # API 엔드포인트 및 라우터
│   ├── core/               # 핵심 설정 (Config, Security, Exceptions)
│   ├── crud/               # DB CRUD 작업
│   ├── db/                 # DB 세션 및 베이스 모델
│   ├── models/             # SQLAlchemy 모델 정의
│   ├── schemas/            # Pydantic 스키마 (Request/Response)
│   └── main.py             # 앱 진입점
├── uploads/                # 로컬 업로드 디렉토리 (개발용)
├── compose.yml             # Docker Compose 설정 (Prod)
├── compose.dev.yml         # Docker Compose 설정 (Dev)
├── Dockerfile              # Docker 이미지 빌드 설정
└── requirements.txt        # Python 의존성 목록
```

## 🔒 보안 및 인증

- **JWT 인증**: 모든 보호된 엔드포인트는 `Authorization: Bearer <token>` 헤더를 요구합니다.
- **토큰 검증**: Auth Server의 JWKS(JSON Web Key Set)를 사용하여 JWT 서명을 검증합니다.
- **CORS**: 허용된 오리진에서의 요청만 처리합니다.

## 📝 라이선스

This project is licensed under the MIT License.
