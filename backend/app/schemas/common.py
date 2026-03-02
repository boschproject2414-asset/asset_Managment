from datetime import datetime

from pydantic import BaseModel


class ORMBase(BaseModel):
    model_config = {'from_attributes': True}


class Message(ORMBase):
    detail: str


class Pagination(ORMBase):
    page: int
    page_size: int
    total: int


class AuditLogRead(ORMBase):
    id: int
    action: str
    actor_id: int | None
    tool_id: int | None
    ticket_id: int | None
    metadata_json: str | None
    timestamp: datetime
