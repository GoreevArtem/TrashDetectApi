from fastapi import APIRouter, status, Depends
from typing import Optional, List

from schemas import schemas
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


@router.get(
    '/get_request',
    status_code=status.HTTP_200_OK,
    response_model=Optional[List[schemas.Request]]
)
async def get_request(
        limit: int = 10,
        request_service: RequestService = Depends()
):
    return request_service.get_request(limit)
