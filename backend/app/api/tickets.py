from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.enums import ApprovalStatus, TicketStatus, ToolStatus, UserRole
from app.models.ticket import Ticket
from app.models.tool import Tool
from app.models.user import User
from app.schemas.ticket import TicketCreate, TicketDecision, TicketRead, TicketReturn
from app.services.audit_service import log_action

router = APIRouter(prefix='/tickets', tags=['tickets'])


@router.post('', response_model=TicketRead)
def create_ticket(payload: TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tool = db.query(Tool).filter(Tool.id == payload.tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail='Tool not found')
    if tool.status == ToolStatus.ISSUED:
        raise HTTPException(status_code=400, detail='Tool already issued')

    ticket = Ticket(
        **payload.model_dump(),
        requested_by_id=current_user.id,
        user_role=current_user.role,
        status=TicketStatus.REQUESTED,
        approval_status=ApprovalStatus.PENDING,
    )
    db.add(ticket)
    log_action(db, action='ticket_created', actor_id=current_user.id, tool_id=payload.tool_id)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.get('', response_model=list[TicketRead])
def list_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    approval_status: ApprovalStatus | None = Query(default=None),
):
    q = db.query(Ticket)
    if current_user.role != UserRole.ASSET_INCHARGE:
        q = q.filter(Ticket.requested_by_id == current_user.id)
    if approval_status:
        q = q.filter(Ticket.approval_status == approval_status)
    return q.order_by(Ticket.id.desc()).all()


@router.put('/approve/{ticket_id}', response_model=TicketRead)
def approve_ticket(
    ticket_id: int,
    payload: TicketDecision,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    ticket = db.query(Ticket).filter(Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')

    tool = db.query(Tool).filter(Tool.id == ticket.tool_id).first()
    if not tool:
        raise HTTPException(status_code=404, detail='Tool not found')

    if payload.approved:
        if tool.status == ToolStatus.ISSUED:
            raise HTTPException(status_code=400, detail='Tool already issued')
        ticket.approval_status = ApprovalStatus.APPROVED
        ticket.status = TicketStatus.ISSUED
        ticket.issue_date = datetime.now(timezone.utc)
        ticket.issued_by_id = current_user.id
        tool.status = ToolStatus.ISSUED
        action = 'ticket_approved'
    else:
        ticket.approval_status = ApprovalStatus.REJECTED
        ticket.status = TicketStatus.CLOSED
        action = 'ticket_rejected'

    log_action(db, action=action, actor_id=current_user.id, tool_id=ticket.tool_id, ticket_id=ticket.id)
    db.commit()
    db.refresh(ticket)
    return ticket


@router.put('/return', response_model=TicketRead)
def return_ticket(
    payload: TicketReturn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ASSET_INCHARGE)),
):
    ticket = db.query(Ticket).filter(Ticket.id == payload.ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail='Ticket not found')
    if ticket.status != TicketStatus.ISSUED:
        raise HTTPException(status_code=400, detail='Ticket is not in issued state')

    tool = db.query(Tool).filter(Tool.id == ticket.tool_id).first()
    tool.status = ToolStatus.AVAILABLE
    ticket.status = TicketStatus.RETURNED
    ticket.return_date = datetime.now(timezone.utc)

    log_action(db, action='ticket_returned', actor_id=current_user.id, tool_id=ticket.tool_id, ticket_id=ticket.id)
    db.commit()
    db.refresh(ticket)
    return ticket
