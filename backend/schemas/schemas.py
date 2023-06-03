from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, EmailStr


class OrmMode(BaseModel):
    class Config:
        orm_mode = True


class UserBaseSchema(OrmMode):
    name: Optional[str] = None
    email: EmailStr
    password: str


class CreateUserSchema(UserBaseSchema):
    pass


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
    address: str
    photo_names: Optional[str]
    class_trash: Optional[str]


class OperationKind(str, Enum):
    NOTVIEW = 'not view'
    VIEW = 'view'
    CLEAN = 'clean'


class Address(OrmMode):
    address_region: Optional[str]
    address_city: Optional[str]
    address_street: Optional[str]
    address_city_district: Optional[str]
    address_house_number: Optional[str]


class Request(OrmMode):
    id: int
    address: Address
    photo_names: Optional[str]
    class_trash: Optional[str]
    request_date: datetime
    region_operator: Optional[int]
    expert: Optional[str]
    status: Optional[OperationKind]

