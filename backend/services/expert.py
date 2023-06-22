import functools
import os

from fastapi import status, Depends, HTTPException
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session, joinedload

from database import models
from database.db import get_session
from schemas import schemas
from services.auth import AuthService
from services.user import UserService
from utils import utils
from utils.JWT import JWTBearer


class Expert(AuthService):

    def __init__(self, session: Session = Depends(get_session)):
        super().__init__(session)

    def __get_expert(
            self,
            payload: schemas.ExpertSchema
    ):
        return self.session.query(models.Expert).filter(or_(
            models.Expert.login == payload.login,
            models.Expert.name == payload.name
        )
        ).first()

    def register_new_expert(
            self,
            payload: schemas.RegisterExpertSchema
    ) -> schemas.ExpertSchema:
        if self.__get_expert(payload) is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Account already exist'
            )

        expert = models.Expert()

        reg_operator_id = self.session.query(models.RegionOperator.id). \
            filter(models.RegionOperator.reg_oper_name == payload.region_operator).first()

        if reg_operator_id is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Region operator not found'
            )

        expert.password = utils.hash_password(payload.password)
        expert.name = payload.name
        expert.login = payload.login
        expert.verified = True
        expert.region_operator_id = functools.reduce(lambda x: x, reg_operator_id)

        self.session.add(expert)
        self.session.commit()
        self.session.refresh(expert)
        return expert

    def authenticate_expert(
            self,
            payload: schemas.ExpertSchema,
    ) -> schemas.TokenSchema:
        expert = self.__get_expert(payload)
        self._not_user(expert)
        self._user_verified(expert)
        self._verify_password(payload, expert)
        access_token = self._create_token(user=expert)
        return schemas.TokenSchema(access_token=access_token)


class ExpertService(UserService):
    def __init__(self, token=Depends(JWTBearer()), session: Session = Depends(get_session)):
        super().__init__(token, session)

    def __get_me(
            self
    ):
        expert = self.session.query(models.Expert). \
            options(joinedload(models.Expert.region_operator)).get(self.user_id)
        if expert is not None:
            return expert
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not authenticated'
            )

    def get_me(
            self
    ):
        expert = self.__get_me()
        expert.__dict__["region_operator"] = expert.__dict__["region_operator"].__dict__["reg_oper_name"]
        return expert

    def update_me(
            self,
            payload: schemas.UpdateExpertSchema
    ):
        user = self.__get_me()
        if payload.password is not None:
            if utils.verify_password(payload.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='The old password has been entered'
                )
            user.password = utils.hash_password(payload.password)

            self.session.commit()
            self.session.refresh(user)

    def get_all_requests(self, limit: int = 10):
        user = self.__get_me()
        try:
            all_requests = self.session.query(models.Request).options(
                joinedload(models.Request.address),
                joinedload(models.Request.expert),
                joinedload(models.Request.region_operator)
            ).order_by(models.Request.id). \
                filter(models.Request.expert_id == user.id).limit(limit).all()
            for request in all_requests:
                request.__dict__["expert"] = request.__dict__["expert"].__dict__["name"]
                request.__dict__["region_operator"] = request.__dict__["region_operator"].__dict__["reg_oper_name"]
            return dict(zip(range(1, len(all_requests) + 1), all_requests))
        except:
            return None

    def get_request(self, req_id: int):
        try:
            user = self.__get_me()
            request = self.session.query(models.Request).options(
                joinedload(models.Request.address),
                joinedload(models.Request.expert),
                joinedload(models.Request.region_operator)
            ).filter(and_(models.Request.id == req_id, models.Request.expert_id == user.id)).first()
            request.__dict__["expert"] = request.__dict__["expert"].__dict__["name"]
            request.__dict__["region_operator"] = request.__dict__["region_operator"].__dict__["reg_oper_name"]
            return request
        except:
            return None

    def get_photo(self, req_id: int):
        user = self.__get_me()
        request = self.session.query(models.Request).filter(and_(models.Request.id == req_id,
                                                                 models.Request.expert_id == user.id)).first()
        os.chdir(os.path.join("..", "source_users_photo"))
        path = os.path.join("..", "source_users_photo", str(request.user_id), str(request.photo_names))
        if os.path.exists(path):
            return path
        else:
            raise HTTPException(status_code=404, detail="Photo not found")

    def set_status(self, req_id: int, status: str):
        user = self.__get_me()
        data = self.session.query(models.Request).filter(and_(models.Request.id == req_id,
                                                              models.Request.expert_id == user.id)).first()
        if data is not None:
            if data.status != status:
                data.status = status
                self.session.commit()
                self.session.refresh(data)
            return data
        else:
            raise HTTPException(status_code=404, detail="Not found")
