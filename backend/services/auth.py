import time

from fastapi import status, Depends, HTTPException
from jose import jwt
from pydantic import EmailStr
from sqlalchemy.orm import Session

from database import models
from database.db import get_session
from schemas import schemas
from settings.settings import settings
from utils import utils


class AuthService:

    def __init__(
            self,
            session: Session = Depends(get_session),

    ):
        self.session = session

    def __get_user_by_email(
            self,
            payload: schemas.UserBaseSchema,
    ):
        return self.session.query(models.User).filter(
            models.User.email == EmailStr(payload.email)
        ).first()

    def __get_user_by_name(
            self,
            payload: schemas.UserBaseSchema,
    ):
        return self.session.query(models.User).filter(
            models.User.name == payload.name).first()

    @staticmethod
    def _not_user(user):
        if not user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect your data')

    @staticmethod
    def _user_verified(user):
        if not user.verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Please verify your email address')

    @staticmethod
    def _verify_password(payload, user):
        if not utils.verify_password(payload.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect your data')

    @staticmethod
    def _create_token(user):
        payload = {
            "user_id": str(user.id),
            "expires": time.time() + settings.ACCESS_TOKEN_EXPIRES_IN * 60
        }
        access_token = jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return access_token

    @staticmethod
    def _delete_token(user, access_token):
        del access_token[str(user.id)]

    def register_new_user(
            self,
            payload: schemas.CreateUserSchema
    ) -> schemas.UserResponseSchema:
        if self.__get_user_by_email(payload) or self.__get_user_by_name(payload):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Account already exist'
            )
        payload.password = utils.hash_password(payload.password)
        payload.email = EmailStr(payload.email)

        new_user = models.User(**payload.dict())
        new_user.role = 'user'
        new_user.verified = True

        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user

    def authenticate_user(
            self,
            payload: schemas.LoginUserSchema,
    ) -> schemas.TokenSchema:
        user = self.__get_user_by_email(payload)
        self._not_user(user)
        self._user_verified(user)
        self._verify_password(payload, user)
        access_token = self._create_token(user=user)
        return schemas.TokenSchema(access_token=access_token)
