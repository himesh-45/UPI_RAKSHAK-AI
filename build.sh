#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> [Render Build] Upgrading pip and installing Python dependencies..."
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "==> [Render Build] Installing Node.js frontend dependencies..."
cd frontend
npm install

echo "==> [Render Build] Building production React assets with Vite..."
npm run build
cd ..

echo "==> [Render Build] Ensuring database directory exists..."
mkdir -p backend/data

echo "==> [Render Build] Build completed successfully!"
