#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. In GitHub Codespaces use a Docker-enabled machine type and retry."
  exit 1
fi

if [[ "${1:-}" == "--down" ]]; then
  docker compose down
  exit 0
fi

if [[ "${1:-}" == "--backend-only" ]]; then
  echo "Starting backend stack in Docker (postgres + backend)..."
  docker compose up --build postgres backend
  exit 0
fi

echo "Starting full stack in Docker (postgres + backend + frontend)..."
docker compose up --build
