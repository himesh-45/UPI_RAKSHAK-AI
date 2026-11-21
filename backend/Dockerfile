FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Tesseract with Hindi & Telugu language packs
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-hin \
    tesseract-ocr-tel \
    libgl1 \
    libglib2.0-0 \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure dataset and model exist
RUN python -m app.scripts.generate_dataset && \
    python -m app.scripts.train_model && \
    python -m app.scripts.generate_demo_assets && \
    python -m app.scripts.seed_db

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
