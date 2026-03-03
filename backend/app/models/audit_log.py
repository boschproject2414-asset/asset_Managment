from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id: Mapped[int] = mapped_column(primary_key=True)
    action: Mapped[str] = mapped_column(String(120), nullable=False)
    actor_id: Mapped[int | None] = mapped_column(ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    tool_id: Mapped[int | None] = mapped_column(ForeignKey('tools.id', ondelete='SET NULL'), nullable=True)
    ticket_id: Mapped[int | None] = mapped_column(ForeignKey('tickets.id', ondelete='SET NULL'), nullable=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)

    actor = relationship('User')
    tool = relationship('Tool')
    ticket = relationship('Ticket')
