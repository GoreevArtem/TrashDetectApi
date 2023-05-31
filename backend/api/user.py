from fastapi import APIRouter, Response, status
from fastapi import Depends

from schemas import schemas
from services.user import UserService
from utils import oauth2

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


@router.get('/me', response_model=schemas.UserResponseSchema)
def get_me(
        user_service: UserService = Depends()
):
    return user_service.get_me()


@router.patch(
    '/me_update',
    status_code=status.HTTP_204_NO_CONTENT
)
def update_me(
        response: Response,
        payload: schemas.UpdateUserSchema,
        user_service: UserService = Depends()
):
    return user_service.update_me(response, payload)


@router.delete('/me_delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_me(
        user_service: UserService = Depends()
):
    user_service.delete_me()
