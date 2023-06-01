import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ARRAY, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    verified = Column(Boolean, nullable=False, server_default='False')
    role = Column(String, server_default='user', nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    requests = relationship('Request', back_populates = "user")


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String)
    request_date = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text("now()"))

    class_trash = Column(String)

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates = "requests")

    status = Column(Boolean, default=False)

#
#
# class Requests(Base):
#     __tablename__ = 'requests'
#
#     id = Column(Integer, primary_key=True, index=True)
#
#     user_id = Column(Integer, ForeignKey(User.id))
#     request_id = Column(Integer, ForeignKey(Request.id))
#
#     status = Column(Boolean, nullable=False, default=False)
#
#
# class Expert(User):
#     __tablename__ = 'expert'
#     role = Column(String, server_default='expert', nullable=False)
#
#
# class Region_Operator(Base):
#     __tablename__ = 'region_operator'
#
#     id = Column(Integer, primary_key=True, index=True)
#     reg_oper_name = Column(String, nullable=False)
#     reg_oper_number_zone = Column(Integer, nullable=False)
#     reg_oper_meaning = Column(String, nullable=False)
