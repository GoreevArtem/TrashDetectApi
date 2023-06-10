import functools

from fastapi import Response, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_
from sqlalchemy.orm import Session

from database import models
from database.db import get_session
from schemas import schemas
from services.auth import AuthService
from services.user import UserService
from utils import utils, oauth2


class Expert(AuthService):

    def __init__(self, session: Session = Depends(get_session), Authorize: AuthJWT = Depends()):
        super().__init__(session, Authorize)

    def __get_user(
            self,
            payload: schemas.ExpertSchema
    ):
        return self.session.query(models.Expert).filter(or_(
            models.Expert.login == payload.login,
            models.Expert.name == payload.name
        )
        ).first()

    def register_new_user(
            self,
            payload: schemas.RegisterExpertSchema
    ) -> schemas.ExpertSchema:
        if self.__get_user(payload) is not None:
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

    def authenticate_user(
            self,
            payload: schemas.ExpertSchema,
            response: Response,

    ) -> schemas.TokenSchema:
        expert = self.__get_user(payload)
        self._not_user(expert)
        self._user_verified(expert)
        self._verify_password(payload, expert)
        access_token = self._create_token(user=expert, response=response)
        # Send both access
        return schemas.TokenSchema(access_token=access_token)

    def logout(self, response: Response):
        self.Authorize.unset_jwt_cookies()
        response.set_cookie('logged_in', '', -1)
        return {'status': 'success'}


class ExpertService(UserService):
    def __init__(
            self,
            user_id: int = Depends(oauth2.require_expert),
            session: Session = Depends(get_session),
            Authorize: AuthJWT = Depends()):
        super().__init__(user_id, session, Authorize)

    def get_me(
            self
    ):
        return self.session.query(models.Expert).get(self.user_id)

    def update_me(
            self,
            response: Response,
            payload: schemas.UpdateExpertSchema
    ):
        user = self.get_me()
        if payload.password is not None:
            if utils.verify_password(payload.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='The old password has been entered'
                )
            user.password = utils.hash_password(payload.password)

            self.Authorize.unset_jwt_cookies()
            response.set_cookie('logged_in', '', -1)

            self.session.commit()
            self.session.refresh(user)
