from datetime import date, datetime

from pydantic import BaseModel

from app.models.enums import ToolOwnership, ToolStatus


class ToolBase(BaseModel):
    tool_code: str
    tool_name: str
    category: str
    location: str
    ownership: ToolOwnership
    status: ToolStatus = ToolStatus.AVAILABLE
    calibration_due_date: date | None = None


class ToolCreate(ToolBase):
    pass


class ToolUpdate(BaseModel):
    tool_name: str | None = None
    category: str | None = None
    location: str | None = None
    ownership: ToolOwnership | None = None
    status: ToolStatus | None = None
    calibration_due_date: date | None = None


class ToolRead(ToolBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}
