from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    name: Optional[str] = None
    email: EmailStr

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    password: str
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(UserBaseSchema):
    # email: EmailStr
    password: str


class UserResponse(UserBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'
