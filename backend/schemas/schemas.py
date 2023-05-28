from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBaseSchema(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class CreateUserSchema(UserBaseSchema):
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(UserBaseSchema):
    # email: EmailStr
    password: str


class UpdateUserSchema(UserBaseSchema):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]


class UserResponseSchema(UserBaseSchema):
    # id: int
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'
