from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBaseSchema(BaseModel):
    # name: Optional[str] = None
    name: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(UserBaseSchema):
    password: str


class UpdateUserSchema(UserBaseSchema):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserResponseSchema(UserBaseSchema):
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
