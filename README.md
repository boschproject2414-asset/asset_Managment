# Bosch Asset / Tool Management System

Production-ready full-stack system for issuing and returning tools across internal projects and external departments.

## Stack
- Backend: FastAPI, SQLAlchemy, PostgreSQL, Alembic, JWT auth.
- Frontend: React + TypeScript (Vite), TailwindCSS, Material UI packages, Axios.

## Key Capabilities
- Role-based authentication (Asset Incharge, Internal Team, External Department).
- Tool lifecycle management (available, issued, maintenance, calibration).
- Trolley management with tool mapping.
- Ticket workflow (request, approve/reject, issue, return).
- Audit logs, overdue alerts, calibration due alerts.
- Search/filter/pagination APIs.

## Project Structure
- `backend/app/models` SQLAlchemy models.
- `backend/app/api` REST endpoints.
- `backend/app/schemas` Pydantic request/response contracts.
- `backend/alembic` migrations.
- `frontend/src/pages` app pages.
- `frontend/src/services` API clients.

## Installation Guide (local/manual, optional)

Recommended for Codespaces: use the Docker-only section below (`npm run codespace:run`) so you do not install Python/Node dependencies on the host VM.

### 1) Start PostgreSQL
```bash
docker compose up -d postgres
```

### 2) Backend setup
```bash
cd backend
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python seed.py
uvicorn app.main:app --reload --port 8000
```

### 3) Frontend setup
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

### 4) Seed users
- Asset Incharge: `admin@bosch.local` / `Admin@123`
- Internal Team: `internal@bosch.local` / `Internal@123`
- External Department: `external@bosch.local` / `External@123`



## Run in GitHub Codespaces (stable, Docker-only)
Use Docker Compose to run everything inside containers (no host Python/Node installs).

### 1) Start app (from repo root)
```bash
npm run codespace:run
```
This starts in detached mode:
- `postgres` on `5432` (database)
- FastAPI backend on `8000`
- Vite frontend on `5173`

### 2) Open the right ports in Codespaces
- Open `5173` for the app UI
- Open `8000` for API health (`/health`)
- **Do not open `5432` in browser** (that is Postgres; browser shows 502 there)

### 3) Logs / stop
```bash
npm run codespace:logs
npm run codespace:down
```

### 4) Quick checks
```bash
curl http://localhost:8000/health
curl -I http://localhost:5173
```

## Run in GitHub Cloud (No local installs)
If your local machine blocks downloads, run the system checks directly in GitHub Actions:

1. Push this repository to GitHub.
2. Open **Actions** tab.
3. Run workflow **Cloud Backend Smoke** (manual `workflow_dispatch`) or open a PR to trigger it.
4. Workflow provisions PostgreSQL service, runs Alembic migrations + seed, boots FastAPI, and executes API smoke tests.

Workflow file: `.github/workflows/cloud-backend-smoke.yml`.
- Optional fallback workflow for beginners: `Cloud Backend Manual Run` (`.github/workflows/cloud-backend-manual.yml`) with manual-only trigger.
- New manual cloud runner: `Cloud Backend Open Tool` (`.github/workflows/cloud-backend-open-tool.yml`) to boot backend in GitHub Actions and optionally run smoke checks.
Smoke script: `scripts/cloud_backend_smoke.sh`.


### If Cloud Backend Smoke fails
- Open the failed workflow run in **Actions**.
- Open job **backend-smoke** and inspect step **Auth and business smoke test**.
- Download artifact **backend-smoke-logs** from the run summary (contains DB prepare log + `api.log`).
- Re-run the workflow using **Re-run all jobs** after fixing env/secrets/config.

## Core APIs
- Auth: `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- Tools: `GET/POST/PUT/DELETE /api/v1/tools`
- Tickets: `POST /api/v1/tickets`, `GET /api/v1/tickets`, `PUT /api/v1/tickets/approve/{ticket_id}`, `PUT /api/v1/tickets/return`
- Trolley: `POST /api/v1/trolley`, `GET /api/v1/trolley`
- Audit: `GET /api/v1/audit`
- Notifications: `GET /api/v1/notifications`

## Security and business rules
- JWT access token with role-based access control.
- Only Asset Incharge can approve/reject/return tickets and manage users/tools.
- Tool cannot be issued if already in issued status.
- Return flow auto-updates ticket/tool state.



## Permanent Clickable URL Deployment (Render)
Use Render to host a permanent backend API URL and frontend URL.

### A) One-time Render setup (no local terminal)
1. In Render dashboard, click **New +** -> **Blueprint**.
2. Connect your GitHub repo and select this repository.
3. Render will detect `render.yaml` and create:
   - `asset-management-api` (FastAPI backend)
   - `asset-management-ui` (frontend static site via `type: web` + `env: static`)
   - `asset-management-db` (PostgreSQL)
4. After first deploy, update frontend env var `VITE_API_URL` in Render Static Service settings to your real backend URL:
   - `https://asset-management-api.onrender.com/api/v1`
5. Redeploy frontend service.

### B) Auto deploy from GitHub Actions (optional)
Workflow: `.github/workflows/deploy-render.yml`

Set these GitHub repository secrets:
- `RENDER_BACKEND_DEPLOY_HOOK_URL`
- `RENDER_FRONTEND_DEPLOY_HOOK_URL`

Then run workflow **Deploy to Render** from Actions tab (or push to `main`).

