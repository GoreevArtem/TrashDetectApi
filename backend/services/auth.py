from datetime import timedelta

from fastapi import APIRouter, Request, Response, status, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
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
            Authorize: AuthJWT = Depends()
    ):
        self.session = session
        self.Authorize = Authorize

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
                                detail='Incorrect Email or Password')

    @staticmethod
    def _user_verified(user):
        if not user.verified:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Please verify your email address')

    @staticmethod
    def _verify_password(payload, user):
        if not utils.verify_password(payload.password, user.password):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail='Incorrect Email or Password')

    def _create_token(self, user, response):
        access_token = self.Authorize.create_access_token(
            subject=str(user.id), expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN))

        refresh_token = self.Authorize.create_refresh_token(
            subject=str(user.id), expires_time=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_IN))

        # Store refresh and access tokens in cookie
        response.set_cookie('access_token', access_token, settings.ACCESS_TOKEN_EXPIRES_IN * 60,
                            settings.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('refresh_token', refresh_token,
                            settings.REFRESH_TOKEN_EXPIRES_IN * 60, settings.REFRESH_TOKEN_EXPIRES_IN * 60, '/',
                            None, False, True, 'lax')
        response.set_cookie('logged_in', 'True', settings.ACCESS_TOKEN_EXPIRES_IN * 60,
                            settings.ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
        return access_token

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
            response: Response,

    ) -> schemas.TokenSchema:
        user = self.__get_user_by_email(payload)
        self._not_user(user)
        self._user_verified(user)
        self._verify_password(payload, user)
        access_token = self._create_token(user=user, response=response)
        # Send both access
        return schemas.TokenSchema(access_token=access_token)

    def refresh_token(self, response: Response) -> schemas.TokenSchema:
        try:
            self.Authorize.jwt_refresh_token_required()

            user_id = self.Authorize.get_jwt_subject()
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='Could not refresh access token')
            user = self.session.query(models.User).filter(models.User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                    detail='The user belonging to this token no logger exist')
            access_token = self.Authorize.create_access_token(
                subject=str(user.id), expires_time=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRES_IN))
        except Exception as e:
            error = e.__class__.__name__
            if error == 'MissingTokenError':
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail='Please provide refresh token')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=error)

        response.set_cookie('access_token', access_token, settings.ACCESS_TOKEN_EXPIRES_IN * 60,
                            settings.
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, True, 'lax')
        response.set_cookie('logged_in', 'True', settings.ACCESS_TOKEN_EXPIRES_IN * 60,
                            settings.
                            ACCESS_TOKEN_EXPIRES_IN * 60, '/', None, False, False, 'lax')
        return schemas.TokenSchema(access_token=access_token)

    def logout(self, response: Response):
        self.Authorize.unset_jwt_cookies()
        response.set_cookie('logged_in', '', -1)
        return {'status': 'success'}
