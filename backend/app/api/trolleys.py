from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.enums import UserRole
from app.models.tool import Tool
from app.models.trolley import Trolley
from app.models.trolley_tool import TrolleyTool
from app.models.user import User
from app.schemas.trolley import AssignToolRequest, TrolleyCreate, TrolleyRead
from app.services.audit_service import log_action

router = APIRouter(prefix='/trolley', tags=['trolley'])


@router.get('', response_model=list[TrolleyRead])
def list_trolleys(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return db.query(Trolley).order_by(Trolley.id.desc()).all()


@router.post('', response_model=TrolleyRead)
def create_trolley(
    payload: TrolleyCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    trolley = Trolley(**payload.model_dump())
    db.add(trolley)
    log_action(db, action='trolley_created', actor_id=current_user.id, metadata=payload.model_dump())
    db.commit()
    db.refresh(trolley)
    return trolley


@router.post('/{trolley_id}/assign')
def assign_tool(
    trolley_id: int,
    payload: AssignToolRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    trolley = db.query(Trolley).filter(Trolley.id == trolley_id).first()
    tool = db.query(Tool).filter(Tool.id == payload.tool_id).first()
    if not trolley or not tool:
        raise HTTPException(status_code=404, detail='Trolley or tool not found')
    exists = db.query(TrolleyTool).filter(TrolleyTool.trolley_id == trolley_id, TrolleyTool.tool_id == payload.tool_id).first()
    if exists:
        raise HTTPException(status_code=400, detail='Tool already assigned')
    db.add(TrolleyTool(trolley_id=trolley_id, tool_id=payload.tool_id))
    log_action(db, action='tool_assigned_to_trolley', actor_id=current_user.id, tool_id=tool.id, metadata={'trolley_id': trolley_id})
    db.commit()
    return {'detail': 'Assigned'}


@router.delete('/{trolley_id}/tools/{tool_id}')
def remove_tool(
    trolley_id: int,
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    link = db.query(TrolleyTool).filter(TrolleyTool.trolley_id == trolley_id, TrolleyTool.tool_id == tool_id).first()
    if not link:
        raise HTTPException(status_code=404, detail='Mapping not found')
    db.delete(link)
    log_action(db, action='tool_removed_from_trolley', actor_id=current_user.id, tool_id=tool_id, metadata={'trolley_id': trolley_id})
    db.commit()
    return {'detail': 'Removed'}
