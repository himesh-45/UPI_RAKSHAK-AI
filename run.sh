#!/usr/bin/env bash
set -e

echo "=========================================================="
echo " Starting UPI Rakshak AI (Zero-Config Local Launcher)"
echo "=========================================================="

# 1. Backend Setup
if [ ! -d ".venv" ]; then
    echo "[1/4] Creating Python virtual environment..."
    python3 -m venv .venv
fi

echo "[2/4] Ensuring Python dependencies..."
source .venv/bin/activate
pip install -q -r backend/requirements.txt

# Ensure models & assets exist
if [ ! -f "backend/app/data/nlp_scam_model.pkl" ]; then
    echo "Training ML model and generating demo dataset..."
    python -m backend.app.scripts.generate_dataset
    python -m backend.app.scripts.train_model
    python -m backend.app.scripts.generate_demo_assets
    python -m backend.app.scripts.seed_db
fi

# 2. Frontend Setup
echo "[3/4] Ensuring Frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
cd ..

# 3. Launch both services
echo "[4/4] Launching Backend on :8000 and Frontend on :5173..."

uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

cd frontend
npm run dev -- --host 0.0.0.0 --port 5173 &
FRONTEND_PID=$!
cd ..

trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT SIGTERM

echo ""
echo "🚀 UPI Rakshak AI is running!"
echo "   Frontend Web UI : http://localhost:5173"
echo "   Backend API Docs: http://localhost:8000/docs"
echo "   Admin Login     : admin@upirakshak.ai / AdminRakshak#2026"
echo ""
echo "Press Ctrl+C to stop both servers."

wait
