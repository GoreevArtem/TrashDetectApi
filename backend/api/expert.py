from fastapi import APIRouter, status, Response, Depends

from schemas import schemas
from services.expert import Expert, ExpertService

router = APIRouter(
    prefix='/expert',
    tags=['expert'],
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ExpertSchema
)
async def create_user(
        payload: schemas.RegisterExpertSchema,
        auth_service: Expert = Depends()
):
    return auth_service.register_new_user(payload)


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


##
# TODO UPDATE SCHEMAS
##
@router.get('/me', status_code=status.HTTP_200_OK)
def get_me(
        expert_service: ExpertService = Depends()
):
    return expert_service.get_me()


@router.patch(
    '/me_update',
    status_code=status.HTTP_204_NO_CONTENT
)
def update_me(
        payload: schemas.UpdateExpertSchema,
        response: Response,
        expert_service: ExpertService = Depends()
):
    return expert_service.update_me(response, payload)


@router.get(
    '/get_requests'
)
def get_requests(expert_service: ExpertService = Depends()):
    ...


def get_request():
    ...


def change_request():
    ...
