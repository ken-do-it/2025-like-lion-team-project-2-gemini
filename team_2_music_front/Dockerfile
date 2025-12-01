# # Build stage
# FROM node:20-alpine as builder

# WORKDIR /app

# # Install dependencies
# COPY package*.json ./
# RUN npm ci

# # Copy source code
# COPY . .

# # Build the application
# RUN npm run build

# # Production stage
# FROM nginx:alpine

# # Copy built assets from builder stage
# COPY --from=builder /app/dist /usr/share/nginx/html

# # Copy nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/default.conf

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]



# ---------- Build stage ----------
FROM node:20-alpine AS builder

WORKDIR /app

# 빌드에 필요한 툴 설치 (native 모듈, git 의존 패키지 대비)
RUN apk add --no-cache python3 make g++ git

# 패키지 설치 (CI + 재현성 위해 npm ci 권장)
COPY package*.json ./
RUN npm ci

# 소스 복사 & 빌드
COPY . .
RUN npm run build

# ---------- Production stage ----------
FROM nginx:alpine

WORKDIR /usr/share/nginx/html

# 기본 설정 제거(선택)
RUN rm /etc/nginx/conf.d/default.conf || true

# 빌드 결과물 복사
COPY --from=builder /app/dist ./

# nginx 설정 복사 (SPA 라우팅)
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
