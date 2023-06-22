from typing import Dict, Optional

from fastapi import APIRouter, status, Depends, HTTPException, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from redis.commands.json.path import Path

from database.redis import redis_startup
from schemas import schemas
from services.expert import Expert, ExpertService

router = APIRouter(
    prefix='/expert',
)


@router.post(
    '/register',
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.ExpertSchema,
    tags=['expert'],
)
async def create_user(
        payload: schemas.RegisterExpertSchema,
        auth_service: Expert = Depends()
):
    return auth_service.register_new_expert(payload)


@router.post(
    '/authenticate',
    status_code=status.HTTP_200_OK,
    response_model=schemas.TokenSchema,
    tags=['expert'],
)
async def authenticate_user(
        payload: schemas.ExpertSchema,
        auth_service: Expert = Depends(),
):
    return auth_service.authenticate_expert(payload)


##
# TODO UPDATE SCHEMAS
##
@router.get(
    '/me',
    status_code=status.HTTP_200_OK,
    response_model=schemas.ExpertData,
    tags=['expert'],
)
def get_me(
        expert_service: ExpertService = Depends()
):
    return expert_service.get_me()


@router.patch(
    '/me_update',
    status_code=status.HTTP_204_NO_CONTENT,
    tags=['expert'],
)
def update_me(
        payload: schemas.UpdateExpertSchema,
        expert_service: ExpertService = Depends()
):
    return expert_service.update_me(payload)


@router.get(
    '/get_all_requests/{limit}',
    status_code=status.HTTP_200_OK,
    response_model=Optional[Dict[str, schemas.RequestExpert]],
    tags=['expert requests'],
)
def get_requests(limit: int, expert_service: ExpertService = Depends()):
    if limit < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='negative parameter')
    key = str(expert_service.user_id) + "_get_requests_expert_" + str(limit)
    if redis_startup.json().get(key) is None:
        data = expert_service.get_all_requests(limit)
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 15)
    return redis_startup.json().get(key)


@router.get(
    '/get_request/{req_id}',
    status_code=status.HTTP_200_OK,
    response_model=Optional[schemas.RequestExpert],
    tags=['expert requests'],
)
def get_request(req_id: int, expert_service: ExpertService = Depends()):
    if req_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='negative parameter')
    key = str(expert_service.user_id) + "_get_request_expert_" + str(req_id)
    if redis_startup.json().get(key) is None:
        data = expert_service.get_request(req_id)
        if data is not None:
            redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
            redis_startup.expire(key, 15)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Not found'
            )
    return redis_startup.json().get(key)


@router.get(
    '/get_photo/{req_id}',
    response_class=FileResponse,
    tags=['expert requests']
)
def download_photo(req_id: int, expert_service: ExpertService = Depends()):
    if req_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='negative parameter')
    return expert_service.get_photo(req_id)


@router.put(
    '/set_view_status/{req_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageSent,
    tags=['expert requests'],
)
def set_view_status(
        req_id: int,
        background_tasks: BackgroundTasks,
        expert_service: ExpertService = Depends()
):
    if req_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='negative parameter')
    background_tasks.add_task(expert_service.set_status, req_id, "view")
    return {"message": "status changed to view"}


@router.put(
    '/set_clean_status/{req_id}',
    status_code=status.HTTP_200_OK,
    response_model=schemas.MessageSent,
    tags=['expert requests'],
)
def set_clean_status(
        req_id: int,
        background_tasks: BackgroundTasks,
        expert_service: ExpertService = Depends()
):
    if req_id < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='negative parameter')
    background_tasks.add_task(expert_service.set_status, req_id, "clean")
    return {"message": "status changed to clean"}
