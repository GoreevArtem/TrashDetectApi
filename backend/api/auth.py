from fastapi import APIRouter, Response, status, Depends

from schemas import schemas
from services.auth import AuthService
from services.user import JWTBearer

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponseSchema
)
async def create_user(
        payload: schemas.CreateUserSchema,
        auth_service: AuthService = Depends()
):
    return auth_service.register_new_user(payload)


@router.post(
    '/authenticate',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenSchema
)
async def authenticate_user(
        payload: schemas.LoginUserSchema,
        auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(payload)
