import functools
import os.path
from typing import List, Optional, Dict

import aiofiles as aiofiles
from fastapi import Depends, HTTPException, status, UploadFile, File
from sqlalchemy import func
from sqlalchemy.orm import joinedload

import utils.create_sourse
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

            get_reqion_operator = self.session.query(models.ZoneRegion).distinct().filter(
                models.ZoneRegion.zone_address_region == address_list[1],
                models.ZoneRegion.zone_address_city == address_list[-4],
                models.ZoneRegion.zone_address_city_district == address_list[-3]
            ).first()

            if get_reqion_operator is not None:
                get_reqion_operator = self.session.query(models.RegionOperator).get(get_reqion_operator.region_operator)
                get_reqion_operator.requests.extend([request])
                self.session.add(get_reqion_operator)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Region operator not found'
                )
            min_count_active_requests = self.session.query(func.min(models.Expert.count_active_requests)).filter(
                models.Expert.region_operator_id == get_reqion_operator.id).first()
            if min_count_active_requests is not None:
                min_count_active_requests = functools.reduce(lambda x: x, min_count_active_requests)
                expert = self.session.query(models.Expert).filter(
                    models.Expert.region_operator_id == get_reqion_operator.id,
                    models.Expert.count_active_requests == min_count_active_requests
                ).first()
                expert.count_active_requests += 1
                expert.requests.extend([request])
                self.session.add(expert)
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Expert not found'
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
                .options(
                joinedload(models.Request.address),
                joinedload(models.Request.region_operator),
                joinedload(models.Request.expert)
            ) \
                .filter(models.Request.user_id == self.user_id) \
                .order_by(models.Request.id) \
                .limit(limit).all()
            for region_operator in data:
                region_operator.__dict__["expert"] = \
                    region_operator.__dict__["expert"].__dict__["name"]
                region_operator.__dict__["expert"] = None
                region_operator.__dict__["region_operator"] = \
                    region_operator.__dict__["region_operator"].__dict__["reg_oper_name"]

            return dict(zip(range(1, len(data) + 1), data))
        except:
            return None

    async def detect_trash_on_photo(self, file: UploadFile = File(...)) -> Dict:
        file.filename = utils.create_sourse.rename_photo(self.user_id, file.filename)
        os.chdir(os.path.join("..", "source_users_photo"))
        utils.create_sourse.create_dir(str(self.user_id))
        file_location = os.path.join("..", "source_users_photo", str(self.user_id), file.filename)
        async with aiofiles.open(file_location, 'wb') as f:
            contents = file.file.read()
            await f.write(contents)

        return {
            "name_photo": file.filename,
            "trash_classes": "1, 2, 3"
        }

    def download_photo(self, upload_name):
        os.chdir(os.path.join("..", "source_users_photo"))
        return os.path.join("..", "source_users_photo", str(self.user_id), upload_name)
