# ==========================================
# UPI Rakshak AI - Production Unified Dockerfile
# Multi-stage: Node.js (Vite React) + Python 3.11 (FastAPI)
# ==========================================

# Stage 1: Build React Frontend (or use pre-built dist)
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend

COPY frontend/ ./
RUN if [ ! -f dist/index.html ]; then npm install --include=optional && npm run build; fi

# Stage 2: Python Backend Runtime
FROM python:3.11-slim AS runner
WORKDIR /app

# Install system dependencies (Tesseract OCR for English, Hindi, Telugu)
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-hin \
    tesseract-ocr-tel \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r ./backend/requirements.txt

# Copy backend application code and data
COPY backend ./backend

# Copy compiled frontend distribution from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Ensure persistent data directory exists for SQLite
RUN mkdir -p /app/backend/data

ENV PORT=8000
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:${PORT}/api/health || exit 1

CMD ["sh", "-c", "uvicorn backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
