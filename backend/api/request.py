from fastapi import APIRouter, Response, status, Depends

from schemas import schemas
from services.auth import AuthService
from services.request import RequestService

router = APIRouter(
    prefix='/request',
    tags=['request'],
)


@router.post(
    '/create_request',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreateRequest
)
async def create_request(
        new_request: schemas.CreateRequest,
        request_service: RequestService = Depends()
):
    return request_service.create_new_request(new_request)
