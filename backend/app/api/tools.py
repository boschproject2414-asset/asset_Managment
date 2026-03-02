from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.enums import ToolStatus, UserRole
from app.models.tool import Tool
from app.models.user import User
from app.schemas.tool import ToolCreate, ToolRead, ToolUpdate
from app.services.audit_service import log_action

router = APIRouter(prefix='/tools', tags=['tools'])


@router.get('', response_model=list[ToolRead])
def list_tools(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
    search: str | None = Query(default=None),
    status: ToolStatus | None = Query(default=None),
    category: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
):
    q = db.query(Tool)
    if search:
        q = q.filter((Tool.tool_code.ilike(f'%{search}%')) | (Tool.tool_name.ilike(f'%{search}%')))
    if status:
        q = q.filter(Tool.status == status)
    if category:
        q = q.filter(Tool.category == category)
    return q.order_by(Tool.id.desc()).offset((page - 1) * page_size).limit(page_size).all()


@router.post('', response_model=ToolRead)
def create_tool(
    payload: ToolCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    exists = db.query(Tool).filter(Tool.tool_code == payload.tool_code).first()
    if exists:
        raise HTTPException(status_code=400, detail='Tool code already exists')
    tool = Tool(**payload.model_dump())
    db.add(tool)
    log_action(db, action='tool_created', actor_id=current_user.id, tool_id=tool.id, metadata={'tool_code': payload.tool_code})
    db.commit()
    db.refresh(tool)
    return tool


@router.put('/{tool_id}', response_model=ToolRead)
def update_tool(
    tool_id: int,
    payload: ToolUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail='Tool not found')
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(tool, key, value)
    log_action(db, action='tool_updated', actor_id=current_user.id, tool_id=tool.id)
    db.commit()
    db.refresh(tool)
    return tool


@router.delete('/{tool_id}')
def delete_tool(
    tool_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    tool = db.query(Tool).filter(Tool.id == tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail='Tool not found')
    db.delete(tool)
    log_action(db, action='tool_deleted', actor_id=current_user.id, metadata={'tool_id': tool_id})
    db.commit()
    return {'detail': 'Deleted'}
