@echo off
echo ==========================================================
echo  Starting UPI Rakshak AI (Windows Launcher)
echo ==========================================================

REM 1. Virtual environment check
if not exist ".venv" (
    echo [1/3] Creating virtual environment...
    python -m venv .venv
)

echo [2/3] Checking dependencies...
call .\.venv\Scripts\activate.bat

if not exist "backend\app\data\nlp_scam_model.pkl" (
    echo Initializing synthetic data and ML models...
    python -m backend.app.scripts.generate_dataset
    python -m backend.app.scripts.train_model
    python -m backend.app.scripts.generate_demo_assets
    python -m backend.app.scripts.seed_db
)

REM 2. Launch Backend in background window
echo [3/3] Starting Backend and Frontend...
start "UPI Rakshak Backend" cmd /c ".venv\Scripts\activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload"

REM 3. Launch Frontend
cd frontend
if not exist "node_modules" (
    call npm install
)
start "UPI Rakshak Frontend" cmd /c "npm run dev -- --host 0.0.0.0 --port 5173"
cd ..

echo.
echo ==========================================================
echo  UPI Rakshak AI is running!
echo    Frontend UI: http://localhost:5173
echo    API Docs:    http://localhost:8000/docs
echo    Admin:       Admin password is in backend/data/.admin_secret (generated on first run)
echo ==========================================================
