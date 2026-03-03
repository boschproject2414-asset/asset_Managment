#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

BACKEND_ONLY=false
if [[ "${1:-}" == "--backend-only" ]]; then
  BACKEND_ONLY=true
fi

cd "$ROOT_DIR"
if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required for Postgres in this setup. In Codespaces, enable Docker support and retry."
  exit 1
fi

echo "[1/6] Starting Postgres..."
docker compose up -d postgres

echo "[2/6] Preparing backend virtualenv and dependencies..."
cd "$BACKEND_DIR"
if [[ ! -d .venv ]]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt >/tmp/backend_pip_install.log 2>&1 || {
  echo "Backend dependency install failed. See /tmp/backend_pip_install.log"
  exit 1
}

if [[ ! -f .env ]]; then
  cp .env.example .env
fi

echo "[3/6] Running migrations and seed..."
alembic upgrade head
python seed.py

echo "[4/6] Starting backend on :8000 ..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 >/tmp/backend_uvicorn.log 2>&1 &
BACKEND_PID=$!

cleanup() {
  if ps -p "$BACKEND_PID" >/dev/null 2>&1; then
    kill "$BACKEND_PID" >/dev/null 2>&1 || true
  fi
}
trap cleanup EXIT

for _ in {1..30}; do
  if curl -fsS http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "Backend is healthy: http://127.0.0.1:8000/health"
    break
  fi
  sleep 1
done

if [[ "$BACKEND_ONLY" == true ]]; then
  echo "[done] Backend-only mode finished. Backend is running in this shell session."
  wait "$BACKEND_PID"
fi

echo "[5/6] Installing frontend dependencies..."
cd "$ROOT_DIR"
npm run frontend:install >/tmp/frontend_npm_install.log 2>&1 || {
  echo "Frontend install failed. See /tmp/frontend_npm_install.log"
  exit 1
}

echo "[6/6] Starting frontend on :5173 ..."
echo "Open forwarded ports in Codespaces: 5173 and 8000"
exec npm run frontend:dev
