from pydantic import BaseModel, EmailStr

from app.models.enums import UserRole


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    role: UserRole
    department: str | None

    model_config = {'from_attributes': True}
