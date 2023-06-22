from typing import Optional, Dict

from fastapi import APIRouter, status, Depends, UploadFile, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from redis.commands.json.path import Path

from database.redis import redis_startup
from schemas import schemas
from services.request import RequestService
from utils.JWT import JWTBearer

router = APIRouter(
    prefix='/request',
    tags=['request'],
)


@router.post(
    '/create_request',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CreateRequest,
    dependencies=[Depends(JWTBearer())]
)
async def create_request(
        new_request: schemas.CreateRequest,
        request_service: RequestService = Depends()
):
    return request_service.create_new_request(new_request)


@router.get(
    '/get_request/{req_id}',
    status_code=status.HTTP_200_OK,
    response_model=Optional[schemas.Request],
    dependencies=[Depends(JWTBearer())]
)
async def get_request(
        req_id: int = Query(ge=0),
        request_service: RequestService = Depends()
):
    key = str(request_service.user_id) + "_get_request_" + str(req_id)
    if redis_startup.json().get(key) is None:
        data = request_service.get_request(req_id)
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 30)
    return redis_startup.json().get(key)


@router.get(
    '/get_requests/{limit}',
    status_code=status.HTTP_200_OK,
    response_model=Optional[Dict[str, schemas.Request]],
    dependencies=[Depends(JWTBearer())]
)
async def get_requests(
        limit: int = Query(default=10, ge=0),
        request_service: RequestService = Depends()
):
    key = str(request_service.user_id) + "_get_all_requests_" + str(limit)
    if redis_startup.json().get(key) is None:
        data = request_service.get_all_requests(limit)
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 30)
    return redis_startup.json().get(key)


@router.post(
    "/detection",
    status_code=status.HTTP_200_OK,
    response_model=Optional[schemas.FindClassTrash],
    dependencies=[Depends(JWTBearer())],
)
async def detect_trash_on_photo(
        file: UploadFile,
        request_service: RequestService = Depends()):
    return await request_service.detect_trash_on_photo(file)


@router.get(
    "/filepath/{upload_name}",
    response_class=FileResponse,
    dependencies=[Depends(JWTBearer())],
)
def download_photo(
        upload_name: str,
        request_service: RequestService = Depends()):
    return request_service.download_photo(upload_name)
