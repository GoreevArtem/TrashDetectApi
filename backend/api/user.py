from typing import Optional

from fastapi import APIRouter, Response, status
from fastapi import Depends

from schemas import schemas
from services.user import UserService, JWTBearer

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/me', dependencies=[Depends(JWTBearer())], status_code=status.HTTP_200_OK,
            response_model= Optional[schemas.UserResponseSchema])
def get_me(
        user_service: UserService = Depends()
):
    return user_service.get_me()


@router.patch(
    '/me_update',
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT
)
def update_me(
        payload: schemas.UpdateUserSchema,
        user_service: UserService = Depends()
):
    return user_service.update_me(payload)


@router.delete(
    '/me_delete',
    dependencies=[Depends(JWTBearer())],
    status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
        user_service: UserService = Depends()
):
    user_service.delete_me()
