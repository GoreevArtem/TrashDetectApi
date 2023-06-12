from datetime import datetime

from fastapi import HTTPException
from fastapi import status, Depends

from database import models
from database.db import Session, get_session
from schemas import schemas
from utils import utils
from utils.JWT import JWTBearer


class UserService:

    def __init__(
            self,
            token=Depends(JWTBearer()),
            session: Session = Depends(get_session),
    ):
        self.token = token
        self.user_id = JWTBearer.decodeJWT(token).get("user_id")
        self.session = session

    def __get_user_by_id(
            self
    ):
        return self.session.query(models.User).get(self.user_id)

    def get_me(
            self
    ):
        return self.__get_user_by_id()

    def delete_me(
            self,
    ):
        user = self.__get_user_by_id()
        self.session.delete(user)
        self.session.commit()

    def update_me(
            self,
            payload: schemas.UpdateUserSchema
    ):
        user = self.__get_user_by_id()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND)
        if payload.name is not None:
            user_name = self.session.query(models.User).filter(models.User.name == payload.name).first()
            if (user_name is not None) and (payload.name == user_name.name):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Name already exist'
                )
            user.name = payload.name

        if payload.password is not None:
            if utils.verify_password(payload.password, user.password):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='The old password has been entered'
                )
            user.password = utils.hash_password(payload.password)

        if payload.email is not None:
            user_email = self.session.query(models.User).filter(models.User.email == payload.email).first()
            if (user_email is not None) and (payload.email == user_email.email):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail='Email already exist'
                )
            user.email = payload.email

        user.updated_at = datetime.now()

        self.session.commit()
        self.session.refresh(user)
