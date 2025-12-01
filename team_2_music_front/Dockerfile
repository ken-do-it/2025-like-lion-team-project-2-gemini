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

# 패키지 설치
COPY package*.json ./
RUN npm ci

# 소스 코드 복사
COPY . .

# 프로덕션 빌드
RUN npm run build

# ---------- Production stage ----------
FROM nginx:alpine

# nginx 기본 설정 제거(선택)
RUN rm /etc/nginx/conf.d/default.conf || true

# 빌드된 정적 파일 복사
COPY --from=builder /app/dist /usr/share/nginx/html

# nginx 설정 복사 (직접 만든 nginx.conf)
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nginx 기본 포트 80 사용
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
