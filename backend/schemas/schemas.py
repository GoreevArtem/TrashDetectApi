from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, EmailStr, Field


class OrmMode(BaseModel):
    class Config:
        orm_mode = True


class UserBaseSchema(OrmMode):
    name: Optional[str] = None
    email: EmailStr
    password: str


class CreateUserSchema(UserBaseSchema):
    role: str = 'user'
    verified: bool = False


class LoginUserSchema(UserBaseSchema):
    password: str


class UpdateUserSchema(UserBaseSchema):
    email: Optional[EmailStr]
    password: Optional[str]


class UserResponseSchema(UserBaseSchema):
    created_at: datetime
    updated_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class CreateRequest(OrmMode):
    # id: int
    address: str
    class_trash: Optional[str]
