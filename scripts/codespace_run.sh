#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. In GitHub Codespaces use a Docker-enabled machine type and retry."
  exit 1
fi

case "${1:-}" in
  --down)
    docker compose down
    exit 0
    ;;
  --logs)
    docker compose logs -f
    exit 0
    ;;
  --backend-only)
    echo "Starting backend stack in Docker (postgres + backend) in detached mode..."
    docker compose up -d --build postgres backend
    ;;
  *)
    echo "Starting full stack in Docker (postgres + backend + frontend) in detached mode..."
    docker compose up -d --build
    ;;
esac

echo "Waiting for backend health..."
for _ in {1..60}; do
  if curl -fsS http://127.0.0.1:8000/health >/dev/null 2>&1; then
    echo "Backend healthy at http://localhost:8000/health"
    break
  fi
  sleep 2
done

echo "Checking frontend..."
for _ in {1..60}; do
  if curl -fsS http://127.0.0.1:5173 >/dev/null 2>&1; then
    echo "Frontend reachable at http://localhost:5173"
    break
  fi
  sleep 2
done

echo "\nDone. In Codespaces, open forwarded ports:"
echo "- 5173 (frontend app)"
echo "- 8000 (backend API)"
echo "Do NOT open 5432 in browser (Postgres port; browser will show 502)."
echo "\nUseful commands:"
echo "- npm run codespace:logs"
echo "- npm run codespace:down"
