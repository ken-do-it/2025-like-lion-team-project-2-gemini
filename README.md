# 🎵 Music Sharing Platform - Team 2

멋쟁이사자처럼 2025 팀 프로젝트 - 음악 공유 SNS 플랫폼

## 📋 프로젝트 개요

음악을 업로드하고 공유하며, 다른 사용자들과 소통할 수 있는 소셜 네트워크 서비스입니다.

## 🏗️ 프로젝트 구조

```
2025-like-lion-team-project-2-gemini/
├── team_2_music_back/     # 백엔드 (FastAPI)
├── team_2_music_front/    # 프론트엔드 (React)
├── compose.dev.yml        # Full Stack 개발용 Docker Compose
└── README.md
```

## 🚀 실행 방법 (Deployment)

### 1. Full Stack 실행 (권장 - 루트 디렉토리)

백엔드와 프론트엔드를 동시에 실행합니다. EC2 배포 시 이 방법을 사용합니다.

```bash
# 프로젝트 루트 디렉토리에서 실행
# (team_2_music_back/.env 파일이 설정되어 있어야 함)

# 개발 모드 (프론트엔드 포트 3000, 백엔드 포트 8000)
docker compose -f compose.dev.yml up -d --build
```

- **Frontend**: `http://localhost:3000` (EC2: `http://<EC2_IP>:3000`)
- **Backend API**: `http://localhost:8000` (EC2: `http://<EC2_IP>:8000`)

### 2. 백엔드만 실행

```bash
cd team_2_music_back
cp .env.example .env
docker compose up -d
```

## 🛠️ 문제 해결 및 개선 사항 (Troubleshooting Log)

개발 과정에서 발생한 주요 이슈와 해결 방법을 상세히 기록했습니다.

### 1. 테스트 실패 해결 (`test_upload_finalize_flow`)
- **문제**: `finalize_upload` 엔드포인트 테스트 시 `artist_name`이 "testuser"가 아닌 "Anonymous"로 설정되는 오류 발생.
- **원인**: 엔드포인트가 `get_optional_user` 의존성을 사용하는데, 테스트 Fixture(`authorized_client`)에서는 `get_current_user`만 오버라이드하고 `get_optional_user`는 오버라이드하지 않음.
- **해결**: `tests/conftest.py`에서 `get_optional_user`도 함께 오버라이드하도록 수정.
  ```python
  # tests/conftest.py
  app.dependency_overrides[get_current_user] = mock_get_current_user
  app.dependency_overrides[get_optional_user] = mock_get_current_user  # 추가됨
  ```

### 2. Pytest 호환성 문제 해결
- **문제**: 테스트 실행 시 `AttributeError: 'Package' object has no attribute 'obj'` 오류 발생하며 실행 불가.
- **원인**: `pytest-asyncio` 최신 버전(1.3.0)과 `pytest` 9.0 간의 호환성 문제.
- **해결**: `pytest-asyncio` 버전을 안정적인 `0.21.1`로 다운그레이드.
  ```bash
  pip install pytest-asyncio==0.21.1
  ```

### 3. Docker 빌드 오류 해결
- **문제**: GitHub Actions CI에서 `npm install` 실패 오류 발생.
- **원인**: 백엔드 `Dockerfile` (`team_2_music_back/Dockerfile`) 하단에 프론트엔드 빌드 단계가 잘못 추가되어 있었음. 백엔드 디렉토리에는 `package.json`이 없으므로 빌드 실패.
- **해결**:
  1. 백엔드 `Dockerfile`에서 잘못된 프론트엔드 빌드 단계 제거.
  2. `.github/workflows/ci.yml`에 프론트엔드 빌드 작업(`build-frontend`)을 별도로 추가하여 CI 파이프라인 분리.

### 4. API URL 중복 문제 해결
- **문제**: 프론트엔드에서 API 호출 시 404 오류 발생. URL이 `http://.../api/v1/api/v1/tracks` 처럼 중복됨.
- **원인**: `src/services/api.js`의 `API_BASE_URL` 설정에 `/api/v1`이 포함되어 있었는데, 개별 API 호출 함수에서도 `/api/v1`을 붙여서 중복 발생.
- **해결**: `API_BASE_URL`을 루트 URL로 수정.
  ```javascript
  // src/services/api.js
  // 변경 전: const API_BASE_URL = 'http://15.165.200.236:8000/api/v1';
  // 변경 후:
  const API_BASE_URL = 'http://15.165.200.236:8000';
  ```

### 5. Docker Compose 경로 문제 해결
- **문제**: 루트에서 `compose.dev.yml` 실행 시 `path not found` 오류 발생.
- **원인**: `compose.dev.yml`이 `team_2_music_back` 폴더 안에 있을 때를 기준으로 작성되어 있어, 프론트엔드 경로가 `./team_2_music_front`로 되어 있었음. (루트 기준으로는 맞지만, 파일이 백엔드 폴더에 있다고 가정된 상태였음 -> 루트로 이동하면서 경로 수정 필요)
- **해결**: 루트 디렉토리에 `compose.dev.yml`을 새로 생성하고, 경로를 명시적으로 지정.
  ```yaml
  # compose.dev.yml
  frontend:
    build:
      context: ./team_2_music_front  # 루트 기준 올바른 경로
  ```

## 🎨 프론트엔드 (team_2_music_front)

### 기술 스택
- **Core**: React 18, Vite
- **Styling**: Tailwind CSS v4
- **State Management**: React Context API (MusicPlayerContext)
- **Networking**: Axios (Interceptors로 JWT 토큰 관리)
- **Routing**: React Router DOM

### 주요 기능
- **음악 재생**: 하단 고정 플레이어, 재생/일시정지, 볼륨/진행바 조절
- **업로드**: 드래그 앤 드롭 지원, 메타데이터 입력
- **반응형 UI**: 모바일 및 데스크탑 지원

## � 백엔드 (team_2_music_back)

### 기술 스택
- **Framework**: FastAPI
- **Database**: PostgreSQL 15, Redis 7
- **Storage**: AWS S3 (Presigned URL)
- **Auth**: JWT (RS256)

## 📦 배포 상태

- **환경**: AWS EC2 (Ubuntu 22.04)
- **URL**:
  - Frontend: `http://15.165.200.236:3000`
  - Backend: `http://15.165.200.236:8000`
- **CI/CD**: GitHub Actions (CI 완료, CD는 수동 배포)

## 📝 라이선스

MIT License