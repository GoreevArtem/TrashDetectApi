from database import models
from fastapi import Response, status, HTTPException, Depends
from schemas import schemas
from utils import oauth2, utils

from .auth import AuthService
from .user import UserService


class Expert(UserService, AuthService):

    def __init__(self, user_id: int = Depends(oauth2.require_expert)):
        super().__init__(user_id)

    def __get_user_by_id(self):
        return self.session.query(models.Expert).get(self.user_id)

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
        user = self.__get_user_by_id()
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
            self
    ):
        return self.__get_user_by_id()
