from typing import List, Optional, Dict

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import joinedload

from database import models
from database.db import Session, get_session
from schemas import schemas
from utils import oauth2
from utils.get_address import get_addr


class RequestService:
    def __init__(
            self,
            session: Session = Depends(get_session),
            user_id: int = Depends(oauth2.require_user)
    ):
        self.session = session
        self.user_id = user_id

    def create_new_request(
            self,
            new_request: schemas.CreateRequest
    ) -> schemas.CreateRequest:
        user = self.session.query(models.User).get(self.user_id)

        request = models.Request()
        address_request = models.Address()

        request.photo_names = new_request.photo_names

        user.requests.extend([request])

        address_list = get_addr(new_request.address)
        if address_list is not None:
            get_id = self.session.query(models.Address).distinct().filter(
                models.Address.address_city == address_list[-4],
                models.Address.address_street == address_list[-2],
                models.Address.address_house_number == address_list[-1]
            ).first()
            if get_id is None:
                address_request.address_region = address_list[1]
                address_request.address_city = address_list[-4]
                address_request.address_city_district = address_list[-3]
                address_request.address_street = address_list[-2]
                address_request.address_house_number = address_list[-1]
                address_request.addresses.extend([request])
                self.session.add_all([user, address_request])
            else:
                request.address_id = get_id.id
                self.session.add(user)

            get_reqion_operator_id = self.session.query(models.ZoneRegion).distinct().filter(
                models.ZoneRegion.zone_address_region == address_list[1],
                models.ZoneRegion.zone_address_city == address_list[-4],
                models.ZoneRegion.zone_address_city_district == address_list[-3]
            ).one_or_none()

            if get_reqion_operator_id is not None:
                get_reqion_operator = self.session.query(models.RegionOperator).get(get_reqion_operator_id.id)
                get_reqion_operator.requests.extend([request])
                self.session.add(get_reqion_operator)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Region operator not found'
                )

            self.session.commit()
            self.session.expire_all()
            return new_request
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Address entered incorrectly'
            )

    def get_request(self, limit: int = 10) -> Optional[Dict[str, schemas.Request]]:
        try:
            data = self.session.query(models.Request) \
                .options(joinedload(models.Request.address), joinedload(models.Request.region_operator)) \
                .filter(models.Request.user_id == self.user_id) \
                .order_by(models.Request.id) \
                .limit(limit).all()
            for region_operator in data:
                region_operator.__dict__["region_operator"] = \
                    region_operator.__dict__["region_operator"].__dict__["reg_oper_name"]
            return dict(zip(range(1, len(data)+1), data))
        except:
            return None

