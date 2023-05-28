from fastapi import Depends, HTTPException
from fastapi import APIRouter, Response, status, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import JSON

from database import models
from database.db import Session, get_session
from schemas import schemas
from utils import oauth2, utils


class UserService:

    def __init__(
            self,
            session: Session = Depends(get_session),
            Authorize: AuthJWT = Depends()
    ):
        self.session = session
        self.Authorize = Authorize

    def __get_user_by_id(
            self,
            user_id: int = Depends(oauth2.require_user)
    ):
        return self.session.query(models.User).filter(models.User.id == user_id).first()

    def get_me(
            self,
            user_id: int
    ):
        return self.__get_user_by_id(user_id)

    def delete_me(
            self,
            user_id: int
    ):
        user = self.__get_user_by_id(user_id)
        self.session.delete(user)
        self.session.commit()

    def update_me(
            self,
            response: Response,
            payload: schemas.UpdateUserSchema,
            user_id: int
    ):
        user: JSON = self.__get_user_by_id(user_id)
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if payload.name is not None:
            user_name: JSON = self.session.query(models.User).filter(models.User.name == payload.name).first()
            if payload.name == user_name.name:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Name already exist'
                )

            payload.name = payload.name

        if payload.password is not None:
            if utils.verify_password(payload.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Old password'
                )
            payload.password = utils.hash_password(payload.password)

        if payload.email is not None:
            user_email: JSON = self.session.query(models.User).filter(models.User.email == payload.email).first()
            if payload.email == user_email.email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Email already exist'
                )
            payload.email = payload.email

        for field, value in payload:
            if value is not None:
                setattr(user, field, value)

        self.Authorize.unset_jwt_cookies()
        response.set_cookie('logged_in', '', -1)

        self.session.commit()
        self.session.refresh(user)