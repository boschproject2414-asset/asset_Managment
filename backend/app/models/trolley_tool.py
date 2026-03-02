from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class TrolleyTool(Base, TimestampMixin):
    __tablename__ = 'trolley_tools'
    __table_args__ = (UniqueConstraint('trolley_id', 'tool_id', name='uq_trolley_tools_trolley_tool'),)

    id: Mapped[int] = mapped_column(primary_key=True)
    trolley_id: Mapped[int] = mapped_column(ForeignKey('trolleys.id', ondelete='CASCADE'), nullable=False, index=True)
    tool_id: Mapped[int] = mapped_column(ForeignKey('tools.id', ondelete='CASCADE'), nullable=False, index=True)

    trolley = relationship('Trolley', back_populates='tools')
    tool = relationship('Tool', back_populates='trolley_links')
