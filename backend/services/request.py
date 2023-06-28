import functools
import os.path
from typing import Optional, Dict

import aiofiles as aiofiles
from fastapi import Depends, HTTPException, status, UploadFile, File
from sqlalchemy import func, and_
from sqlalchemy.orm import joinedload

import utils.create_source
from database import models
from database.db import Session, get_session
from schemas import schemas
from utils.JWT import JWTBearer
from utils.detect import GarbageDetection
from utils.get_address import get_addr


class RequestService:
    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: Session = Depends(get_session),
    ):
        self.token = token
        self.user_id = JWTBearer.decodeJWT(token).get("user_id")
        self.session = session

    def create_new_request(
            self,
            new_request: schemas.CreateRequest
    ) -> schemas.CreateRequest:
        user = self.session.query(models.User).get(self.user_id)

        request = models.Request()
        address_request = models.Address()

        request.photo_names = new_request.photo_names
        request.garbage_classes = new_request.class_trash

        user.requests.extend([request])
        new_request = new_request.address.split(",")
        address_list = get_addr(", ".join([new_request[0], new_request[-2], new_request[-1]]))
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

    def get_request(self, req_id: int) -> Optional[schemas.Request]:
        try:
            data = self.session.query(models.Request) \
                .options(
                joinedload(models.Request.address),
                joinedload(models.Request.region_operator),
                joinedload(models.Request.expert)
            ) \
                .filter(and_(models.Request.user_id == self.user_id, models.Request.id == req_id)).first()
            data.__dict__["expert"] = \
                data.__dict__["expert"].__dict__["name"]
            data.__dict__["region_operator"] = \
                data.__dict__["region_operator"].__dict__["reg_oper_name"]
            return data
        except:
            return None

    def get_all_requests(self, limit: int = 10) -> Optional[Dict[str, schemas.Request]]:
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
                region_operator.__dict__["region_operator"] = \
                    region_operator.__dict__["region_operator"].__dict__["reg_oper_name"]

            return dict(zip(range(1, len(data) + 1), data))
        except:
            return None

    async def detect_trash_on_photo(self, file: UploadFile = File(...)) -> Dict:
        if file.content_type.split("/")[0] != "image":
            raise HTTPException(status_code=400, detail="Invalid file type")
        file.filename = utils.create_source.rename_photo(self.user_id, file.filename)
        os.chdir(os.path.join("..", "source_users_photo"))
        utils.create_source.create_dir(str(self.user_id))
        file_location = os.path.join("..", "source_users_photo", str(self.user_id), file.filename)
        async with aiofiles.open(file_location, 'wb') as f:
            await f.write(file.file.read())
        find_garbage = GarbageDetection(os.path.join("..", "app", "best.pt")).garbage_detection(file_location,
                                                                                                file_location)
        if find_garbage is not None:
            if find_garbage[1] != 0:
                user = self.session.query(models.User).get(self.user_id)
                user.amount_garbage += find_garbage[1]
                self.session.commit()
                self.session.refresh(user)
            return {
                "name_photo": file.filename,
                "trash_classes": find_garbage[0]
            }
        else:
            if os.path.isfile(file_location):
                os.remove(file_location)
            raise HTTPException(status_code=404, detail="Trash not found")

    def download_photo(self, upload_name: str):
        os.chdir(os.path.join("..", "source_users_photo"))
        path = os.path.join("..", "source_users_photo", str(self.user_id), upload_name)
        if os.path.exists(path):
            return path
        else:
            raise HTTPException(status_code=404, detail="Photo not found")
