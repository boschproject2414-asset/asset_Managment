from datetime import date

from sqlalchemy import Date, Enum, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ToolOwnership, ToolStatus


class Tool(Base, TimestampMixin):
    __tablename__ = 'tools'
    __table_args__ = (
        Index('ix_tools_status_category', 'status', 'category'),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    tool_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    tool_name: Mapped[str] = mapped_column(String(160), nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(120), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    ownership: Mapped[ToolOwnership] = mapped_column(Enum(ToolOwnership, name='tool_ownership'), nullable=False)
    status: Mapped[ToolStatus] = mapped_column(Enum(ToolStatus, name='tool_status'), nullable=False, default=ToolStatus.AVAILABLE)
    calibration_due_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    trolley_links = relationship('TrolleyTool', back_populates='tool', cascade='all, delete-orphan')
    tickets = relationship('Ticket', back_populates='tool')
