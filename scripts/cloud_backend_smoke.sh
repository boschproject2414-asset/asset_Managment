#!/usr/bin/env bash
set -euo pipefail

LOGIN_RESP=$(curl -fsS -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@bosch.local","password":"Admin@123"}')

TOKEN=$(LOGIN_RESP="$LOGIN_RESP" python3 - <<'PY'
import json, os
print(json.loads(os.environ['LOGIN_RESP'])['access_token'])
PY
)

TOOLS=$(curl -fsS http://localhost:8000/api/v1/tools \
  -H "Authorization: Bearer ${TOKEN}")

FIRST_TOOL_ID=$(TOOLS="$TOOLS" python3 - <<'PY'
import json, os
items = json.loads(os.environ['TOOLS'])
assert len(items) > 0, 'No tools returned from /tools'
print(items[0]['id'])
PY
)

TODAY=$(date +%F)
RETURN_DATE=$(date -d '+2 day' +%F)

TICKET_PAYLOAD=$(cat <<JSON
{"tool_id": ${FIRST_TOOL_ID}, "department":"Engine Testing", "project":"Project Alpha", "reason":"CI workflow issue validation", "request_date":"${TODAY}", "expected_return_date":"${RETURN_DATE}"}
JSON
)

NEW_TICKET=$(curl -fsS -X POST http://localhost:8000/api/v1/tickets \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d "${TICKET_PAYLOAD}")

TICKET_ID=$(NEW_TICKET="$NEW_TICKET" python3 - <<'PY'
import json, os
print(json.loads(os.environ['NEW_TICKET'])['id'])
PY
)

APPROVE_RESP=$(curl -fsS -X PUT "http://localhost:8000/api/v1/tickets/approve/${TICKET_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H 'Content-Type: application/json' \
  -d '{"approved":true}')

APPROVE_RESP="$APPROVE_RESP" python3 - <<'PY'
import json, os
resp = json.loads(os.environ['APPROVE_RESP'])
assert resp['approval_status'] == 'approved', f"Unexpected approval status: {resp['approval_status']}"
assert resp['status'] == 'issued', f"Unexpected ticket status: {resp['status']}"
print('Smoke test passed')
PY
