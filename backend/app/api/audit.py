from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.models.audit_log import AuditLog
from app.models.enums import UserRole
from app.models.user import User
from app.schemas.common import AuditLogRead

router = APIRouter(prefix='/audit', tags=['audit'])


@router.get('', response_model=list[AuditLogRead])
def list_audit_logs(db: Session = Depends(get_db), _: User = Depends(require_roles(UserRole.ASSET_INCHARGE))):
    return db.query(AuditLog).order_by(AuditLog.id.desc()).limit(200).all()
