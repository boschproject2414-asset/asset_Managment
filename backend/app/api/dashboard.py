from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.enums import ApprovalStatus, TicketStatus, ToolStatus
from app.models.ticket import Ticket
from app.models.tool import Tool

router = APIRouter(prefix='/dashboard', tags=['dashboard'])


@router.get('/summary')
def dashboard_summary(db: Session = Depends(get_db), _=Depends(get_current_user)):
    total = db.query(func.count(Tool.id)).scalar() or 0
    available = db.query(func.count(Tool.id)).filter(Tool.status == ToolStatus.AVAILABLE).scalar() or 0
    issued = db.query(func.count(Tool.id)).filter(Tool.status == ToolStatus.ISSUED).scalar() or 0
    maintenance = db.query(func.count(Tool.id)).filter(Tool.status == ToolStatus.MAINTENANCE).scalar() or 0
    calibration_due = (
        db.query(func.count(Tool.id)).filter(Tool.calibration_due_date.is_not(None), Tool.calibration_due_date <= date.today()).scalar()
        or 0
    )
    pending_tickets = db.query(func.count(Ticket.id)).filter(Ticket.approval_status == ApprovalStatus.PENDING).scalar() or 0
    overdue = (
        db.query(func.count(Ticket.id))
        .filter(Ticket.status == TicketStatus.ISSUED, Ticket.expected_return_date.is_not(None), Ticket.expected_return_date < date.today())
        .scalar()
        or 0
    )

    return {
        'total_tools': total,
        'available': available,
        'issued': issued,
        'maintenance': maintenance,
        'calibration_due': calibration_due,
        'pending_tickets': pending_tickets,
        'overdue_returns': overdue,
    }
