from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ARRAY, ForeignKey
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    verified = Column(Boolean, nullable=False, server_default='False')
    role = Column(String, server_default='user', nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    request_id = Column(Integer, ForeignKey("request.id"))
    requests = relationship("Request", back_populates="user")


class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True, nullable=False)
    address = Column(String, nullable=False)
    request_date = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text("now()"))
    class_trash = Column(String)

    user = relationship("User", back_populates="requests")


class Requests(Base):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id))
    status = Column(Boolean, nullable=False, default=False)
