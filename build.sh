#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> [Render Build] Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> [Render Build] Preparing frontend distribution..."
if [ -f "frontend/dist/index.html" ]; then
    echo "==> [Render Build] Found pre-compiled frontend distribution in frontend/dist. Skipping Node build."
else
    echo "==> [Render Build] Installing Node.js frontend dependencies..."
    cd frontend
    npm install --include=optional
    npm install --no-save @rolldown/binding-linux-x64-gnu@1.2.19 || true

    echo "==> [Render Build] Building production React assets with Vite..."
    npm run build
    cd ..
fi

echo "==> [Render Build] Ensuring database directory exists..."
mkdir -p backend/data

echo "==> [Render Build] Build completed successfully!"
