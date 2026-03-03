from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ApprovalStatus, TicketStatus, UserRole


class Ticket(Base, TimestampMixin):
    __tablename__ = 'tickets'
    __table_args__ = (
        Index('ix_tickets_approval_status_request_date', 'approval_status', 'request_date'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tool_id: Mapped[int] = mapped_column(ForeignKey('tools.id', ondelete='RESTRICT'), nullable=False)
    requested_by_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='RESTRICT'), nullable=False)
    user_role: Mapped[UserRole] = mapped_column(Enum(UserRole, name='ticket_user_role'), nullable=False)
    department: Mapped[str] = mapped_column(String(120), nullable=False)
    project: Mapped[str | None] = mapped_column(String(120), nullable=True)
    trolley_id: Mapped[int | None] = mapped_column(ForeignKey('trolleys.id', ondelete='SET NULL'), nullable=True)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    request_date: Mapped[date] = mapped_column(Date, nullable=False)
    expected_return_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    approval_status: Mapped[ApprovalStatus] = mapped_column(Enum(ApprovalStatus, name='approval_status'), nullable=False, default=ApprovalStatus.PENDING)
    issue_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    return_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    issued_by_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    status: Mapped[TicketStatus] = mapped_column(Enum(TicketStatus, name='ticket_status'), nullable=False, default=TicketStatus.REQUESTED)

    tool = relationship('Tool', back_populates='tickets')
    requester = relationship('User', back_populates='tickets', foreign_keys=[requested_by_id])
    issuer = relationship('User', back_populates='issued_tickets', foreign_keys=[issued_by_id])
    trolley = relationship('Trolley', back_populates='tickets')
