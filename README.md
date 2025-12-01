# 🎵 Music Sharing Platform - Team 2

멋쟁이사자처럼 2025 팀 프로젝트 - 음악 공유 SNS 플랫폼

## 📋 프로젝트 개요

음악을 업로드하고 공유하며, 다른 사용자들과 소통할 수 있는 소셜 네트워크 서비스입니다.

## 🏗️ 프로젝트 구조

```
2025-like-lion-team-project-2-gemini/
├── team_2_music_back/     # 백엔드 (FastAPI)
├── team_2_music_front/    # 프론트엔드 (React)
└── README.md
```

## 🚀 백엔드 (team_2_music_back)

### 기술 스택

- **Framework**: FastAPI
- **Database**: PostgreSQL 15
- **Cache**: Redis 7
- **Storage**: AWS S3
- **Authentication**: JWT (RS256)
- **ORM**: SQLAlchemy
- **Migration**: Alembic
- **Testing**: Pytest
- **Containerization**: Docker & Docker Compose

### 주요 기능

#### ✅ 구현 완료
- **사용자 관리**: 프로필 생성, 조회, 수정
- **음악 업로드**: S3 Presigned URL을 통한 안전한 업로드
- **음악 스트리밍**: Proxy 스트리밍으로 파일 경로 보호
- **소셜 기능**:
  - 좋아요 (Like)
  - 댓글 (Comment)
  - 팔로우 (Follow)
- **플레이리스트**: 생성, 트랙 추가/제거
- **재생 기록**: 자동 기록 및 조회
- **Docker 환경**: 완전한 컨테이너화
- **CI/CD**: GitHub Actions 자동화
- **테스트**: 단위 및 통합 테스트

#### 🔜 예정
- 알림 시스템
- 검색 기능
- 추천 알고리즘

### 실행 방법

#### Docker로 실행 (권장)

```bash
cd team_2_music_back

# 환경 변수 설정
cp .env.example .env
# .env 파일을 편집하여 필요한 값 입력

# Docker Compose로 실행
docker compose up -d

# 로그 확인
docker compose logs -f

# 종료
docker compose down
```

#### 로컬 실행

```bash
cd team_2_music_back

# 가상 환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 마이그레이션
alembic upgrade head

# 서버 실행
uvicorn app.main:app --reload --port 8000
```

### API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 테스트

```bash
# Docker 환경에서 테스트
docker compose exec fastapi pytest

# 로컬 환경에서 테스트
pytest
```

### 데이터베이스 마이그레이션

```bash
# 새 마이그레이션 생성
docker compose exec fastapi alembic revision --autogenerate -m "설명"

# 마이그레이션 적용
docker compose exec fastapi alembic upgrade head

# 마이그레이션 롤백
docker compose exec fastapi alembic downgrade -1
```

## 🎨 프론트엔드 (team_2_music_front)

### 기술 스택
- **Framework**: React
- **(추가 정보 필요)*

## 🔄 CI/CD

GitHub Actions를 통해 자동화된 CI/CD 파이프라인이 구축되어 있습니다:

- **테스트**: 모든 푸시와 PR에서 자동 실행
- **린트**: Flake8을 통한 코드 스타일 검사
- **빌드**: Docker 이미지 빌드 검증

## 📦 배포

- **개발 환경**: Docker Compose
- **프로덕션 환경**: AWS EC2 (예정)

## 👥 팀 멤버

- Team 2

## 📝 라이선스

MIT License

## 📚 참고 문서

- [백엔드 상세 문서](./team_2_music_back/README.md)
- [아키텍처 설계](./team_2_music_back/skill_back_music.md)