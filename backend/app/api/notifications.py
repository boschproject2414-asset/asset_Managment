from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.enums import ApprovalStatus, TicketStatus
from app.models.ticket import Ticket
from app.models.tool import Tool

router = APIRouter(prefix='/notifications', tags=['notifications'])


@router.get('')
def list_notifications(db: Session = Depends(get_db), _=Depends(get_current_user)):
    calibration_alerts = (
        db.query(Tool)
        .filter(Tool.calibration_due_date.is_not(None), Tool.calibration_due_date <= date.today())
        .order_by(Tool.calibration_due_date.asc())
        .limit(20)
        .all()
    )
    overdue_tickets = (
        db.query(Ticket)
        .filter(Ticket.status == TicketStatus.ISSUED, Ticket.expected_return_date.is_not(None), Ticket.expected_return_date < date.today())
        .all()
    )
    pending_tickets = db.query(Ticket).filter(Ticket.approval_status == ApprovalStatus.PENDING).count()

    return {
        'calibration_due': [{'tool_id': t.id, 'tool_code': t.tool_code, 'due_date': t.calibration_due_date} for t in calibration_alerts],
        'overdue_returns': [
            {'ticket_id': t.id, 'tool_id': t.tool_id, 'expected_return_date': t.expected_return_date} for t in overdue_tickets
        ],
        'pending_tickets': pending_tickets,
    }
