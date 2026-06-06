# SAI

Vue 3 + FastAPI 풀스택 웹 서비스

## 페이지 구성

| 경로 | 설명 |
|---|---|
| `/login` | 로그인 |
| `/main` | 메인 대시보드 |
| `/admin` | 관리자 패널 (admin 역할만) |
| `/worldcup` | 이상형 월드컵 |

## 로컬 개발

```bash
# 전체 실행 (Docker Compose)
docker compose up --build

# 개별 실행
cd backend  &&  pip install -r requirements.txt  &&  uvicorn app.main:app --reload
cd frontend &&  npm install  &&  npm run dev
```

기본 계정: `admin / admin1234`, `user1 / user1234`

## CI/CD 구성

`main` 브랜치에 push → GitHub Actions → ECR 이미지 빌드·푸시 → App Runner 자동 배포

### GitHub Repository Variables (Settings → Variables → Actions)

| 변수명 | 예시 |
|---|---|
| `AWS_REGION` | `ap-northeast-2` |
| `ECR_REGISTRY` | `123456789.dkr.ecr.ap-northeast-2.amazonaws.com` |
| `ECR_BACKEND_REPO` | `sai-backend` |
| `ECR_FRONTEND_REPO` | `sai-frontend` |
| `APP_RUNNER_BACKEND_ARN` | `arn:aws:apprunner:...` |
| `APP_RUNNER_FRONTEND_ARN` | `arn:aws:apprunner:...` |

### GitHub Secrets

| 변수명 | 설명 |
|---|---|
| `AWS_ROLE_ARN` | GitHub OIDC용 IAM Role ARN |

### AWS 사전 준비

1. **ECR 저장소** 2개 생성: `sai-backend`, `sai-frontend`
2. **App Runner 서비스** 2개 생성 (ECR 이미지 소스, 포트 8000 / 80)
3. **IAM Role** 생성 — GitHub Actions OIDC Provider 신뢰 정책 + ECR push + App Runner deploy 권한