from datetime import datetime

from pydantic import BaseModel

from app.models.enums import TrolleyStatus


class TrolleyBase(BaseModel):
    trolley_code: str
    project: str
    department: str
    status: TrolleyStatus = TrolleyStatus.ACTIVE


class TrolleyCreate(TrolleyBase):
    pass


class TrolleyUpdate(BaseModel):
    project: str | None = None
    department: str | None = None
    status: TrolleyStatus | None = None


class TrolleyRead(TrolleyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {'from_attributes': True}


class AssignToolRequest(BaseModel):
    tool_id: int


class RemoveToolRequest(BaseModel):
    tool_id: int
