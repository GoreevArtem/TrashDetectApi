from fastapi import APIRouter, Response, status, Depends

from schemas import schemas
from services.auth import AuthService

router = APIRouter(
    prefix='/auth',
    tags=['auth'],
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserResponse
)
async def create_user(
        payload: schemas.CreateUserSchema,
        auth_service: AuthService = Depends()
):
    return auth_service.register_new_user(payload)


@router.post(
    '/authenticate_user',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=schemas.Token
)
async def authenticate_user(
        payload: schemas.LoginUserSchema,
        response: Response,
        auth_service: AuthService = Depends(),
):
    return auth_service.authenticate_user(payload, response)


@router.get(
    '/refresh'
)
def refresh_token(response: Response, auth_service: AuthService = Depends()):
    return auth_service.refresh_token(response)


@router.get(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT
)
def logout(response: Response, auth_service: AuthService = Depends()):
    return auth_service.logout(response)