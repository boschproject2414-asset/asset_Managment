import json
from typing import Any

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog


def log_action(
    db: Session,
    *,
    action: str,
    actor_id: int | None = None,
    tool_id: int | None = None,
    ticket_id: int | None = None,
    metadata: dict[str, Any] | None = None,
) -> None:
    row = AuditLog(
        action=action,
        actor_id=actor_id,
        tool_id=tool_id,
        ticket_id=ticket_id,
        metadata_json=json.dumps(metadata) if metadata else None,
    )
    db.add(row)
