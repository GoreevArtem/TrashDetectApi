from datetime import timedelta

from fastapi import APIRouter, Response, status, HTTPException
from pydantic import EmailStr

from database import models
from database.db import get_session
from schemas import schemas
from settings.settings import settings
from utils import utils

from .auth import AuthService


class Expert(AuthService):
    def __get_user(
            self,
            payload: schemas.ExpertSchema,
    ):
        return self.session.query(models.Expert).filter(
            models.Expert.login == payload.login,
            models.Expert.name == payload.name
        ).first()

    def authenticate_user(
            self,
            payload: schemas.ExpertSchema,
            response: Response,

    ) -> schemas.TokenSchema:
        user = self.__get_user(payload)
        super()._not_user(user)
        super()._user_verified(user)
        super()._verify_password(payload, user)
        access_token = super()._create_token(user=user, response=response)
        return schemas.TokenSchema(access_token=access_token)

    def update_me(
            self,
            response: Response,
            payload: schemas.UpdateUserSchema
    ):
        user = self.session.query(models.Expert).filter(
            models.Expert.login == payload.login
        ).first()
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

    def get_me(
            self,
            payload: schemas.ExpertBaseSchema
    ):
        return self.session.query(models.Expert).filter(
            models.Expert.login == payload.login
        ).first()