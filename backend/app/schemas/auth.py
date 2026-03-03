from pydantic import BaseModel

from app.models.enums import UserRole


class LoginRequest(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserRead(BaseModel):
    id: int
    full_name: str
    email: str
    role: UserRole
    department: str | None

    model_config = {'from_attributes': True}
