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
    return auth_service.register_new_expert(payload)


@router.post(
    '/authenticate',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenSchema
)
async def authenticate_user(
        payload: schemas.ExpertSchema,
        auth_service: Expert = Depends(),
):
    return auth_service.authenticate_expert(payload)


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
        expert_service: ExpertService = Depends()
):
    return expert_service.update_me(payload)


@router.get(
    '/get_all_requests',
    status_code=status.HTTP_200_OK
)
def get_requests(limit: int = 10, expert_service: ExpertService = Depends()):
    return expert_service.get_all_requests(limit)


@router.get(
    '/get_request',
    status_code=status.HTTP_200_OK
)
def get_request(req_id: int, expert_service: ExpertService = Depends()):
    return expert_service.get_request(req_id)


@router.put(
    '/set_view_status',
    status_code=status.HTTP_200_OK
)
def set_view_status(req_id: int, expert_service: ExpertService = Depends()):
    return expert_service.set_view_status(req_id)


def change_request():
    ...
