from typing import Optional, Dict, List

from fastapi import APIRouter, status, Depends, UploadFile, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from redis.commands.json.path import Path

from database.redis import redis_startup
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
    response_model=Optional[Dict[str, schemas.Request]]
)
async def get_request(
        limit: int = Query(default=10, ge=0),
        request_service: RequestService = Depends()
):
    key = str(request_service.user_id) + "_get_request_" + str(limit)
    if redis_startup.json().get(key) is None:
        data = request_service.get_request(limit)
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 30)
    return redis_startup.json().get(key)


@router.post(
    "/detection",
    status_code=status.HTTP_200_OK,
    response_model=Optional[Dict[str, schemas.FindClassTrash]]
)
async def detect_trash_on_photo(
        files: List[UploadFile],
        request_service: RequestService = Depends()):
    data = [schemas.FindClassTrash(**await request_service.detect_trash_on_photo(file)) for file in files]
    return dict(zip(range(1, len(data) + 1), data))


@router.get("/filepath", response_class=FileResponse)
def download_photo(
        upload_name: str,
        request_service: RequestService = Depends()):
    return request_service.download_photo(upload_name)
