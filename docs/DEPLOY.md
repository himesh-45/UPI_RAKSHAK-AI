# UPI Rakshak AI - Production Deployment & Operations Guide

This guide details deployment options for **UPI Rakshak AI**, ranging from single-node Docker containers to high-security air-gapped intranet installations.

---

## 1. Single-Node Docker Compose (Recommended for Hackathon / Production VM)

The fastest and most isolated way to run UPI Rakshak AI in production.

### Prerequisites
- Docker Engine 24.0+ and Docker Compose v2.20+
- 2 CPU cores, 2 GB RAM minimum (4 GB recommended for concurrent OCR)

### Deployment Steps
1. Clone or unpack the repository:
   ```bash
   git clone https://github.com/your-org/upi-rakshak-ai.git
   cd upi-rakshak-ai
   ```

2. Configure environment variables in `.env` (copy from `.env.example`):
   ```bash
   cp .env.example .env
   # Edit .env to set JWT_SECRET, ADMIN_EMAIL, and optional bot credentials
   ```

3. Launch production stack using `docker-compose.prod.yml`:
   ```bash
   docker compose -f docker-compose.prod.yml up -d --build
   ```

4. Verify service status and health checks:
   ```bash
   docker compose -f docker-compose.prod.yml ps
   curl -f http://localhost:8000/api/health
   ```

### Architecture in Production Compose
- **Backend Container (`upi_rakshak_backend_prod`)**: Runs multi-stage Python 3.11 image under an unprivileged user (`appuser`, UID 10001), hardened with `no-new-privileges:true`. Resource limited to 2.0 CPUs and 1.5 GB RAM.
- **Frontend Container (`upi_rakshak_frontend_prod`)**: Nginx Alpine serving optimized static assets and reverse-proxying `/api/` traffic directly to the backend over internal Docker bridge network `rakshak_net`.
- **Persistent Volume (`backend_data`)**: Stores SQLite database (`upi_rakshak.db`) and pre-trained scikit-learn models.

---

## 2. Render Cloud Deployment (Zero-Config / Free Tier)

Deploying UPI Rakshak AI on Render (render.com) provides an instant, public HTTPS URL with automatic builds and zero server maintenance.

### Method A: Blueprint (Recommended - 1-Click via `render.yaml`)
1. Push your repository to GitHub or GitLab.
2. Log in to [dashboard.render.com](https://dashboard.render.com).
3. Click **New +** &rarr; **Blueprint**.
4. Select your `upi-rakshak-ai` repository. Render automatically reads `render.yaml`.
5. Enter any optional secrets (e.g. `TELEGRAM_BOT_TOKEN`), then click **Apply**.
6. Render builds the React frontend and Python backend, then deploys to `https://upi-rakshak-ai.onrender.com`.

### Method B: Manual Web Service Setup
1. On [Render Dashboard](https://dashboard.render.com), click **New +** &rarr; **Web Service**.
2. Connect your GitHub repository.
3. Configure settings:
   - **Name**: `upi-rakshak-ai`
   - **Environment**: `Python 3` (or `Docker` using root `Dockerfile`)
   - **Build Command**: `./build.sh` (or `pip install -r backend/requirements.txt && cd frontend && npm install && npm run build && cd ..`)
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   - `DATABASE_URL`: `sqlite:///./backend/data/upi_rakshak.db`
   - `JWT_SECRET`: `<generated_random_secret>`
   - `ADMIN_EMAIL`: `admin@upirakshak.ai`
   - `SENDER_HASH_SALT`: `<random_salt>`
   - `TELEGRAM_BOT_TOKEN`: `9270859974:AAFkXi6GE9k64x81oPxODkmmDnRu5jj61-Q`
5. Click **Deploy Web Service**.

---

## 3. Serverless Deployment: Google Cloud Run / AWS ECS

Because UPI Rakshak AI is designed with an **in-memory, CPU-optimized ML pipeline** (< 30ms latency, zero GPU requirements), it runs exceptionally well on serverless container platforms.

### Google Cloud Run Deployment
```bash
# 1. Build and push backend image to Google Artifact Registry
gcloud builds submit --tag gcr.io/$PROJECT_ID/upi-rakshak-backend:latest ./backend -f backend/Dockerfile.prod

# 2. Deploy backend service
gcloud run deploy upi-rakshak-backend \
  --image gcr.io/$PROJECT_ID/upi-rakshak-backend:latest \
  --platform managed \
  --region asia-south1 \
  --memory 2Gi \
  --cpu 2 \
  --min-instances 1 \
  --max-instances 10 \
  --set-env-vars="JWT_SECRET=projects/$PROJECT_ID/secrets/jwt-secret" \
  --allow-unauthenticated

# 3. Build & deploy frontend with VITE_API_BASE pointing to Cloud Run backend URL
```

### Key Serverless Characteristics
- **Fast Cold Start**: Pre-compiled TF-IDF vocabulary and Logistic Regression weights load in under 600ms on container boot.
- **Stateless Analysis**: All detection endpoints (`/api/analyze/text`, `/api/analyze/url`, `/api/analyze/qr`) are stateless. Feedback and audit logs persist to SQLite or an external PostgreSQL instance via `DATABASE_URL`.

---

## 3. Air-Gapped & Offline Intranet Installation

For regulated banking intranets (e.g., NPCI internal networks, bank fraud monitoring centers, defense installations) where external internet access is prohibited:

### Export Image Bundle on Internet-Connected Machine
```bash
# Build production images locally
docker compose -f docker-compose.prod.yml build

# Export images to compressed tar archive
docker save \
  upi-rakshak-ai-backend:latest \
  upi-rakshak-ai-frontend:latest \
  | gzip > upi_rakshak_offline_bundle.tar.gz
```

### Import on Air-Gapped Host
```bash
# Transfer archive via approved secure removable media
# Load docker images onto air-gapped host
gunzip -c upi_rakshak_offline_bundle.tar.gz | docker load

# Start services offline
docker compose -f docker-compose.prod.yml up -d --no-build
```

### Offline Guarantees
- **No External CDN**: All frontend dependencies (React, Lucide icons, Recharts) are compiled into self-contained JavaScript/CSS bundles.
- **Local Language Models**: TF-IDF char+word n-gram models and multilingual rule engines run entirely locally.
- **Zero Remote Phishing Queries**: URL scanner uses static algorithmic parsing and local Trie/Levenshtein matching without querying Google Safe Browsing or external APIs.
- **Tesseract OCR In-Container**: Hindi (`hin`), Telugu (`tel`), and English (`eng`) traineddata files are baked directly into the container image.

---

## 4. Security Hardening & Resource Quotas

| Dimension | Specification | Verification |
|---|---|---|
| User Privilege | Unprivileged user `appuser` (UID 10001) | `docker exec <container> id` |
| Capabilities | `cap_drop: [ALL]` with `no-new-privileges` | Docker daemon inspect |
| Memory Limits | Backend: 1536 MB max; Frontend: 512 MB max | Docker cgroups v2 |
| CPU Limits | Backend: 2.0 cores max; Frontend: 1.0 core max | Docker cgroups v2 |
| Rate Limiting | 20 messages / hour sliding window per client hash | Verified by `test_channels.py` |
| PII Masking | 100% phone/account/Aadhaar/UPI masking prior to DB write | Verified by `test_api.py` & `test_masking.py` |
