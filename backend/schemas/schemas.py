from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict

from pydantic import BaseModel, EmailStr


class OrmMode(BaseModel):
    class Config:
        orm_mode = True


class UserBaseSchema(OrmMode):
    name: Optional[str]
    email: EmailStr
    password: str


class CreateUserSchema(UserBaseSchema):
    pass


class LoginUserSchema(UserBaseSchema):
    password: str


class UpdateUserEmailSchema(OrmMode):
    email: EmailStr


class UpdateUserPasswordSchema(OrmMode):
    password: Optional[str]


class UserResponseSchema(OrmMode):
    name: Optional[str]
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    amount_garbage: Optional[int]


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
    garbage_classes: Optional[str]
    request_date: datetime
    region_operator: Optional[str]
    expert: Optional[str]
    status: Optional[OperationKind]


class FindClassTrash(OrmMode):
    name_photo: str
    trash_classes: Optional[Dict[str, int]]


class ExpertBaseSchema(OrmMode):
    login: str


class ExpertSchema(ExpertBaseSchema):
    name: str
    password: str


class RegisterExpertSchema(ExpertSchema):
    region_operator: Optional[str]


class UpdateExpertSchema(OrmMode):
    password: str


class ExpertData(OrmMode):
    login: str
    name: str
    region_operator: str
    count_active_requests: int


class RequestExpertBase(OrmMode):
    id: int
    status: Optional[OperationKind]


class RequestExpert(RequestExpertBase):
    region_operator: str
    expert: str
    request_date: datetime
    photo_names: Optional[str]
    address: Address
