from fastapi import APIRouter, status, Response, Depends

from schemas import schemas
from services.expert import Expert

router = APIRouter(
    prefix='/expert',
    tags=['expert'],
)


@router.post(
    '/authenticate',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenSchema
)
async def authenticate_user(
        payload: schemas.ExpertSchema,
        response: Response,
        auth_service: Expert = Depends(),
):
    return auth_service.authenticate_user(payload, response)


@router.get(
    '/logout',
    status_code=status.HTTP_204_NO_CONTENT
)
def logout(response: Response, auth_service: Expert = Depends()):
    return auth_service.logout(response)


@router.patch(
    '/me_update',
    status_code=status.HTTP_204_NO_CONTENT
)
def update_me(
        payload: schemas.UpdateExpertSchema,
        response: Response,
        user_service: Expert = Depends()
):
    return user_service.update_me(response, payload)

@router.get(
    '/get_me',
    status_code=status.HTTP_200_OK
)
def get_me(
        payload: schemas.ExpertBaseSchema,
        user_service: Expert = Depends()
):
    return user_service.get_me(payload)