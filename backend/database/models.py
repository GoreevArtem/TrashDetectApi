import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ARRAY, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .db import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    verified = Column(Boolean, nullable=False, server_default="False")
    role = Column(String, server_default='user', nullable=False)

    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text("now()"))

    requests = relationship('Request', back_populates="user")


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True, index=True)
    request_date = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text("now()"))

    photo_names = Column(String)
    status = Column(String, default="not view")

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship("User", back_populates="requests")

    region_operator_id = Column(Integer, ForeignKey("region_operator.id"))
    region_operator = relationship("RegionOperator", back_populates="requests")

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship("Address", back_populates="addresses")

    garbage_classes = relationship("GarbageClass", back_populates="request")


class RegionOperator(Base):
    __tablename__ = 'region_operator'

    id = Column(Integer, primary_key=True, index=True)
    reg_oper_name = Column(String, nullable=False)
    reg_oper_number_zone = Column(Integer, nullable=False)
    reg_oper_meaning = Column(String, nullable=False)

    requests = relationship("Request", back_populates="region_operator")
    experts = relationship("Expert", back_populates="region_operator")


class Expert(Base):
    __tablename__ = 'expert'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default="True")

    region_operator_id = Column(Integer, ForeignKey("region_operator.id"))
    region_operator = relationship("RegionOperator", back_populates="experts")


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    address_region = Column(String)
    address_city = Column(String)
    address_city_district = Column(String)
    address_street = Column(String)
    address_house_number = Column(String)

    addresses = relationship('Request', back_populates="address")

    __table_args__ = (
        UniqueConstraint('address_house_number'),
    )


class GarbageClass(Base):
    __tablename__ = 'garbage_class'

    id = Column(Integer, primary_key=True, index=True)
    class_trash = Column(String)

    request_id = Column(Integer, ForeignKey("request.id"))
    request = relationship("Request", back_populates="garbage_classes")


class RegionOperatorAddress(Base):
    __tablename__ = "region_operator_address"
    id = Column(Integer, primary_key=True, index=True)
    address = Column("address_id", Integer, ForeignKey("address.id")),
    region_operator = Column("region_operator_id", Integer, ForeignKey("region_operator.id"))
