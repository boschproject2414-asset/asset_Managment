from datetime import date, datetime

from pydantic import BaseModel

from app.models.enums import ApprovalStatus, TicketStatus, UserRole


class TicketCreate(BaseModel):
    tool_id: int
    department: str
    project: str | None = None
    trolley_id: int | None = None
    reason: str
    request_date: date
    expected_return_date: date | None = None


class TicketDecision(BaseModel):
    approved: bool


class TicketReturn(BaseModel):
    ticket_id: int


class TicketRead(BaseModel):
    id: int
    tool_id: int
    requested_by_id: int
    user_role: UserRole
    department: str
    project: str | None
    trolley_id: int | None
    reason: str
    request_date: date
    expected_return_date: date | None
    approval_status: ApprovalStatus
    issue_date: datetime | None
    return_date: datetime | None
    issued_by_id: int | None
    status: TicketStatus
    created_at: datetime

    model_config = {'from_attributes': True}
