---
name: music-sharing-backend-architect
description: "FastAPI + JWT(Auth Server) + PostgreSQL + Redis + S3 기반 음악 공유 SNS 백엔드 아키텍처/README를 단계별로 설계·업데이트할 때 사용하세요."
version: 0.1.0
---

# Music Sharing Backend Architect Skill

이 스킬은 **음악 공유 SNS 백엔드**를 설계하고,  
FastAPI + JWT(Auth Server) + CORS + PostgreSQL + Redis + S3 + Docker + Nginx + EC2 기반의  
**README.md / 설계 문서**를 단계별로 업데이트할 때 사용한다.

주 목적은 **코드 없이 설계·구조·정책·아키텍처만 정리**하는 것이다.

---

## 1. 이 스킬을 언제 사용해야 하는가

다음과 같은 요청이 있을 때 이 스킬을 사용한다:

- “음악 공유 플랫폼 백엔드 설계해줘”
- “FastAPI + JWT + PostgreSQL로 음악 공유 SNS 만들고 싶은데 README 정리해줘”
- “권한 서버에서 JWT 받아서 퍼블릭키로 검증하는 구조로 백엔드 설계하고 싶어”
- “지금 구조에 ERD, 캐시, 보안, 테스트 전략을 더 추가하고 싶어”
- “Phase 1/2/3 별로 백엔드 설계 업데이트 해줘”

사용자는 다음을 **직접 한다**:

- 라이브러리 설치
- 실제 코드 작성
- 명령어 실행
- 테스트 실행

이 스킬은 **오직 설계/문서**만 담당한다.

---

## 2. 핵심 원칙

1. **백엔드 우선**  
   - FastAPI + JWT + CORS + PostgreSQL + Redis + S3 + Docker + Nginx + EC2 기준으로 설계한다.
   - 프론트(React)는 존재하지만, 이 스킬에서는 **백엔드 관점(설계/인터페이스)**만 다룬다.

2. **권한 서버 분리 + 퍼블릭키 검증**  
   - 로그인/회원가입/토큰 발급은 **별도 Auth Server** 책임.
   - Music API는 **JWT를 퍼블릭키(JWKS, RS256)** 로 검증만 수행한다.
   - 토큰 블랙리스트/발급/갱신은 기본적으로 Auth Server 책임으로 둔다.

3. **코드/명령어 금지**  
   - Python 코드, FastAPI 엔드포인트 구현 코드, shell 명령어를 작성하지 않는다.
   - 필요한 명령어는 **사용자에게 명령어를 실행해달라고 요청**한다.
   - 테스트 확인은 **사용자에게 테스트 명령어를 실행해달라고 요청**한다.
   - 테스트 명령어 실행 후 **사용자에게 테스트 결과를 확인해달라고 요청**한다. 대신 필요한 테스트를 알려준다.
   - 대신 **README용 설계, 구조, 테이블, 체크리스트, 예시 JSON 포맷** 정도까지만 작성한다.

4. **단계별 진행 + 사용자 확인 필수**  
   - 큰 변경 또는 새로운 Phase(예: Phase 1 → Phase 2)를 설계한 후,
     항상 마지막에 “이 설계대로 다음 단계로 진행할까요?”처럼 **사용자 확인을 요청**한다.
   - 사용자가 “좋아/응/계속” 등으로 승인하면 다음 단계 설계로 확장한다.

5. **하나의 README/MD 파일 기준**  
   - 결과물은 항상 “하나의 README.md 또는 SKILL.md 파일로 쓸 수 있는 구조”가 되도록 작성한다.
   - 여러 파일로 쪼개지 말고, 하나의 문서 안에 목차/섹션으로 정리한다.

---

## 3. 목표 시스템 요약

- 음악 공유 SNS:
  - 음악 업로드/스트리밍
  - 좋아요, 댓글
  - 팔로우/피드
  - 플레이리스트
  - 재생 기록
  - 알림
- 인증:
  - 별도 Auth Server
  - JWT (RS256, access token 위주)
  - Music API는 JWT 검증 + 권한 체크만 수행
- 백엔드:
  - FastAPI
  - SQLAlchemy + Alembic
  - Redis(캐시 + JWKS 캐시)
  - PostgreSQL
  - AWS S3 (presigned upload/download)
- 인프라:
  - Docker + Docker Compose
  - AWS EC2
  - Nginx (reverse proxy + HTTPS)
  - GitHub Actions (CI/CD)

---

## 4. 문서 구조 설계 가이드

사용자가 README/설계 문서를 원하면, 기본적으로 아래 구조를 사용한다:

1. 프로젝트 개요
2. 전체 아키텍처 (Auth Server + Music API + Frontend + S3 + Redis + DB)
3. 기술 스택
4. Database Schema (ERD + 인덱스 + 삭제 정책)
5. Backend Skills(모듈) 설명 (Claude의 Skill 개념과 유사한 도메인 모듈)
6. Music Upload Flow (3단계 업로드 + 비동기 처리)
7. Error Handling 규칙
8. Caching 전략 (Redis)
9. API Versioning & 문서화
10. 환경 설정(dev/staging/prod)
11. 테스트 전략
12. 보안 체크리스트
13. 로깅 & 모니터링
14. 백업 & 장애 복구 전략
15. 확장성(Scalability) 계획
16. 개발 단계(Phase별 계획)

요청에 따라 이 중 일부만 뽑아서 작성할 수도 있고,
전체를 한 번에 작성할 수도 있다.

---

## 5. Database 설계 가이드

### 5.1 ERD 개요

다음 관계를 유지한다:

- `UserProfile (1) ↔ (N) Track`
- `UserProfile (1) ↔ (N) Comment`
- `UserProfile (1) ↔ (N) PlayHistory`
- `UserProfile (1) ↔ (N) Playlist`
- `Track (1) ↔ (N) Like`
- `Track (1) ↔ (N) Comment`
- `Track (N) ↔ (N) Tag` (중간 테이블 `TrackTag`)
- `Playlist (N) ↔ (N) Track` (중간 테이블 `PlaylistTrack`)
- `UserProfile (N) ↔ (N) UserProfile` (중간 테이블 `Follow`)

### 5.2 인덱스 전략

- Track: `created_at DESC`, `owner_user_id`, `(title, artist_name)`, `trending_score`
- Like: `UNIQUE(track_id, user_id)`, `track_id`
- Comment: `track_id`, `created_at DESC`
- Tag: `UNIQUE(name)`
- TrackTag: `UNIQUE(track_id, tag_id)`, `tag_id`
- Follow: `UNIQUE(follower_id, following_id)`, `following_id`
- PlayHistory: `user_id`, `played_at DESC`

### 5.3 삭제 정책

- User: Soft delete (계정 비활성화, 데이터 보존)
- Track 삭제 시: Like, Comment, PlaylistTrack, PlayHistory는 cascade 삭제 또는 soft delete
- Playlist 삭제 시: PlaylistTrack cascade 삭제
- Tag는 기본적으로 삭제하지 않고, 관계만 삭제

---

## 6. Backend “Skills” (도메인 모듈) 목록

각 도메인 모듈을 Claude Skills처럼 생각하고, README에서는 “Skill” 또는 “Module”로 표현한다.

### 6.1 `auth-jwt-verify`

- 역할: Auth Server에서 발급한 JWT(access token)를 RS256 공개키로 검증
- 기능:
  - Authorization 헤더 파싱: `Bearer <token>`
  - JWT 서명/만료 검증
  - `sub`, `roles`, `email` 등 클레임 추출
- JWKS/공개키는 Redis에 캐싱 (TTL 1시간)
- 실패 시 401 + 표준 에러 포맷 응답

### 6.2 `user-profile`

- 역할: 플랫폼 내부 사용자 프로필 관리
- 기능:
  - `GET /users/me`, `GET /users/{id}`
  - `PATCH /users/me` 닉네임/소개/프로필 이미지 수정
- `UserProfile`은 Auth Server의 user_id와 1:1 매핑

### 6.3 `user-follow-system`

- 역할: 팔로우/언팔로우 + 팔로워/팔로잉 리스트
- API 예시:
  - `POST /users/{id}/follow`
  - `DELETE /users/{id}/follow`
  - `GET /users/{id}/followers`
  - `GET /users/{id}/following`
- 규칙:
  - 자기 자신 팔로우 불가
  - `UNIQUE(follower_id, following_id)`로 중복 방지

### 6.4 `music-upload`

- 역할: presigned URL 기반 음악 업로드
- 3단계 플로우:
  1. `POST /tracks/upload/initiate` → `upload_id` + `presigned_url` 반환
  2. 프론트가 `presigned_url`로 S3에 직접 업로드
  3. `POST /tracks/upload/finalize` → DB에 Track 생성
- 비동기 후처리:
  - duration, BPM, waveform, 썸네일 처리 (Celery 등으로 확장 가능)

### 6.5 `music-streaming-basic`

- 역할: 재생용 메타데이터 + URL 제공
- 기능:
  - `GET /tracks/{id}` → 트랙 정보 + 재생 URL
  - 필요 시 S3 presigned GET URL 발급

### 6.6 `interaction-like-comment`

- 역할: 좋아요/댓글
- 기능:
  - 좋아요 토글: `POST /tracks/{id}/like`, `DELETE /tracks/{id}/like`
  - 댓글 CRUD: `GET/POST/PATCH/DELETE /comments`
- 알림 시스템과 연동 가능

### 6.7 `tag-search-discovery`

- 역할: 검색/탐색
- 기능:
  - 쿼리, 태그, mood 기반 검색
  - 최신/인기 정렬

### 6.8 `recommendation-basic`

- 역할: 간단한 추천 기능
- 데이터 기반:
  - Like, Tag, PlayHistory
- 초기: rule-based (내가 좋아한 태그가 많이 붙은 트랙 추천)

### 6.9 `playlist-management`

- 역할: 플레이리스트 생성/관리/공개
- 기능:
  - 플레이리스트 CRUD
  - 트랙 추가/삭제/순서 변경
  - 다른 사람 플레이리스트 fork

### 6.10 `play-history-tracking`

- 역할: 재생 이력 기록
- 기능:
  - `POST /tracks/{id}/play`
  - `GET /users/me/history`
- 비로그인 사용자는 이력 저장하지 않음

### 6.11 `notification-system`

- 역할: 알림(좋아요/댓글/팔로우/업로드)
- 기능:
  - `GET /notifications`
  - 읽음 처리
- 실시간(WebSocket/SSE)은 추후 확장

### 6.12 `admin-moderation`

- 역할: 관리자용 콘텐츠/사용자 제재
- 기능:
  - 신고 관리
  - 트랙 숨김/삭제
  - 계정 밴

---

## 7. Music Upload Flow 상세 설명

문서에 아래 패턴으로 설명한다:

1. **Initiate**  
   - 입력: filename, content_type, file_size  
   - 출력: `upload_id`, `presigned_url`, `expires_in`  
   - 백엔드가 `upload_id`를 메모리 또는 DB에 임시 저장할 수 있다.

2. **Upload to S3**  
   - 프론트 → S3로 PUT  
   - Music API는 관여하지 않는다.

3. **Finalize**  
   - 입력: `upload_id`, title, tags, 기타 메타데이터  
   - DB에 Track 생성 (`status=processing`)  
   - 후처리 완료 후 `ready` 상태로 변경 가능

4. **에러/롤백 전략**  
   - finalize 없이 방치된 `upload_id` 정리 (clean-up job)  
   - S3에만 올라가고 DB에는 없는 “고아 파일” 정리 정책 정의

---

## 8. Error Handling 전략

문서에 다음 원칙을 넣는다:

- 표준 에러 JSON 포맷 사용
- HTTP Status 코드를 일관되게 사용
- FastAPI의 ValidationError도 래핑해서 같은 포맷으로 반환

에러 유형 예:

- `TRACK_NOT_FOUND`
- `UNAUTHORIZED`
- `FORBIDDEN`
- `VALIDATION_FAILED`
- `DUPLICATE_RESOURCE`
- `FILE_UPLOAD_FAILED`

---

## 9. Caching 전략

Redis 사용처를 설명한다:

- JWKS / 퍼블릭키 캐싱 (TTL 1h)
- Track 메타데이터 (TTL 5m)
- Trending Feed (TTL 1m)
- User Profile (TTL 10m)
- Hot Tracks (TTL 5m)

Redis 장애 시에는 **캐시 미스 → DB or Auth Server Fallback**을 기본 전략으로 명시한다.

---

## 10. API 버전 & 문서화

- 모든 엔드포인트는 `/api/v1/...` 형태
- major breaking change 시 `/api/v2` 병행 운영
- FastAPI의 OpenAPI/Swagger `/docs` 사용
- README에 “문서에서 확인해야 할 항목”을 체크리스트로 제공:
  - 모든 엔드포인트가 `/docs` 에 노출되는지
  - 에러 포맷 예제가 문서화되어 있는지
  - Authorization 헤더 사용법이 명시되어 있는지

---

## 11. 환경 분리

환경별로 다른 설정을 README에 정리한다:

- dev: 로컬 DB/Redis, dev Auth Server, dev S3
- staging: RDS small, staging S3, staging Auth Server
- prod: RDS(Multi-AZ, 백업), prod S3, prod Auth Server, 모니터링 활성화

환경변수는:

- 로컬: `.env`
- 서버: SSM Parameter Store / Secrets Manager
- CI/CD: GitHub Secrets

---

## 12. 테스트 전략

README에 다음을 포함한다:

- Unit Test: 핵심 로직(JWT 검증, 업로드 플로우, DB CRUD)
- Integration Test: 실제 API 흐름(인증 → 비즈니스 로직 → 응답)
- E2E(선택): 프론트까지 포함한 전체 사용자 시나리오
- GitHub Actions에서:
  - PR 생성 시 자동 테스트
  - 실패 시 merge 불가

---

## 13. 보안 체크리스트

README의 보안 섹션에서 아래 항목을 체크리스트로 제공한다:

- RS256 JWT, 올바른 만료 시간
- Access/Refresh 역할 분리 (Refresh는 Auth Server 책임)
- Track/Comment/Playlist 수정 권한 체크
- CORS 허용 도메인 제한
- Rate Limiting (예: 60 req/min)
- 민감 정보 로그 비노출
- S3 Bucket Public 비활성화
- Security Group 최소 권한 원칙

---

## 14. 로깅 & 모니터링

README에 다음 내용을 포함한다:

- JSON 구조화 로그 예시
- 모니터링 해야 할 지표:
  - API 에러율
  - DB 쿼리 시간
  - Redis hit ratio
  - S3 업로드 실패율
  - CPU/메모리

---

## 15. 백업 & 재해 복구

문서에 포함할 내용:

- RDS 자동 백업 + 스냅샷 정책
- S3 versioning 활성화
- 복구 시나리오 (DB 복구 → S3 복구 → 인프라 재구축 순서)
- 정기적인 DR 훈련 계획

---

## 16. 확장성(Scalability) 고려

README의 확장성 섹션에 아래 내용을 요약한다:

- Music API 서버 수평 확장 (Auto Scaling)
- ALB + Nginx
- Redis Cluster
- CloudFront CDN
- 향후 마이크로서비스 분리:
  - Auth Server
  - Recommendation Service
  - Streaming Service

---

## 17. 단계별(Phase) 진행 가이드

사용자가 “Phase 1만 먼저” 또는 “Phase 2 설계도 정리해줘”라고 하면,  
아래 가이드를 참고해 해당 섹션만 집중적으로 작성한다:

- Phase 1: Auth 구조 + 베이스 아키텍처
- Phase 2: Track/Upload/Streaming + Profile
- Phase 3: Follow/Feed/Like/Comment/Playlist/History/Notification
- Phase 4: Docker/배포/인프라 정리
- Phase 5: 성능 최적화, Admin, Background Tasks, 확장성

각 Phase 설계가 끝날 때마다:

> “이 설계 그대로 다음 Phase 설계도 진행할까요?”  

라고 물어보고,  
사용자가 동의하면 다음 Phase 설계를 이어서 작성한다.

---
