import uuid

from sqlalchemy import Column, Integer, String, TIMESTAMP, text, Boolean, ARRAY, ForeignKey, Table, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, backref

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

    requests = relationship(
        'Request',
        back_populates="user"
    )


class Request(Base):
    __tablename__ = 'request'

    id = Column(Integer, primary_key=True, index=True)
    request_date = Column(TIMESTAMP(timezone=True),
                          nullable=False, server_default=text("now()"))

    photo_names = Column(String)
    status = Column(String, default="not view")

    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship(
        "User",
        back_populates="requests"
    )

    region_operator_id = Column(Integer, ForeignKey("region_operator.id"))
    region_operator = relationship(
        "RegionOperator",
        back_populates="requests"
    )

    address_id = Column(Integer, ForeignKey("address.id"))
    address = relationship(
        "Address",
        back_populates="addresses"
    )

    garbage_classes = relationship(
        "GarbageClass",
        back_populates="request"
    )
    expert_id = Column(UUID(as_uuid=True), ForeignKey("expert.id"))
    expert = relationship(
        "Expert",
        back_populates="requests"
    )


class RegionOperator(Base):
    __tablename__ = 'region_operator'

    id = Column(Integer, primary_key=True, index=True)
    reg_oper_name = Column(String, nullable=False)
    reg_oper_number_zone = Column(Integer, nullable=False)
    reg_oper_meaning = Column(String, nullable=False)

    zone_region = relationship(
        'ZoneRegion',
        back_populates="region"
    )

    requests = relationship(
        "Request",
        back_populates="region_operator"
    )
    experts = relationship(
        "Expert",
        back_populates="region_operator"
    )


class ZoneRegion(Base):
    __tablename__ = 'zone_region'
    id = Column(Integer, primary_key=True, index=True)
    zone_address_region = Column(String)
    zone_address_city = Column(String)
    zone_address_city_district = Column(String)
    region_operator = Column(Integer, ForeignKey("region_operator.id"))
    region = relationship(
        'RegionOperator',
        back_populates="zone_region"
    )


class Expert(Base):
    __tablename__ = 'expert'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    verified = Column(Boolean, nullable=False, server_default="True")
    count_active_requests = Column(Integer)

    region_operator_id = Column(Integer, ForeignKey("region_operator.id"))
    region_operator = relationship(
        "RegionOperator",
        back_populates="experts"
    )

    requests = relationship(
        'Request',
        back_populates="expert"
    )


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True)
    address_region = Column(String)
    address_city = Column(String)
    address_city_district = Column(String)
    address_street = Column(String)
    address_house_number = Column(String, unique=True)

    addresses = relationship(
        'Request',
        back_populates="address"
    )


class GarbageClass(Base):
    __tablename__ = 'garbage_class'

    id = Column(Integer, primary_key=True, index=True)
    class_trash = Column(String)

    request_id = Column(Integer, ForeignKey("request.id"))
    request = relationship("Request", back_populates="garbage_classes")
