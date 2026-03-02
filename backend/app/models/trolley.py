from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import TrolleyStatus


class Trolley(Base, TimestampMixin):
    __tablename__ = 'trolleys'

    id: Mapped[int] = mapped_column(primary_key=True)
    trolley_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    project: Mapped[str] = mapped_column(String(120), nullable=False)
    department: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[TrolleyStatus] = mapped_column(Enum(TrolleyStatus, name='trolley_status'), nullable=False, default=TrolleyStatus.ACTIVE)

    tools = relationship('TrolleyTool', back_populates='trolley', cascade='all, delete-orphan')
    tickets = relationship('Ticket', back_populates='trolley')
