from typing import Dict, Optional

from fastapi import APIRouter, status, Depends, HTTPException, Query
from fastapi.encoders import jsonable_encoder
from fastapi.responses import FileResponse
from redis.commands.json.path import Path
from sqlalchemy.orm import Session

from database.db import get_session
from database.redis import redis_startup
from schemas import schemas
from services.expert import Expert, ExpertService, set_status

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
    '/get_all_requests',
    status_code=status.HTTP_200_OK,
    response_model=Optional[Dict[str, schemas.RequestExpert]],
    tags=['expert requests'],
)
def get_requests(limit: int = Query(default=10, ge=0), expert_service: ExpertService = Depends()):
    key = str(expert_service.user_id) + "_get_requests_expert_" + str(limit)
    if redis_startup.json().get(key) is None:
        data = expert_service.get_all_requests(limit)
        redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
        redis_startup.expire(key, 30)
    return redis_startup.json().get(key)


@router.get(
    '/get_request',
    status_code=status.HTTP_200_OK,
    response_model=Optional[schemas.RequestExpert],
    tags=['expert requests'],
)
def get_request(req_id: int = Query(ge=0), expert_service: ExpertService = Depends()):
    key = str(expert_service.user_id) + "_get_request_expert_" + str(req_id)
    if redis_startup.json().get(key) is None:
        data = expert_service.get_request(req_id)
        if data is not None:
            redis_startup.json().set(key, Path.root_path(), jsonable_encoder(data))
            redis_startup.expire(key, 30)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Not found'
            )
    return redis_startup.json().get(key)


@router.get(
    '/get_photo',
    response_class=FileResponse,
    tags=['expert requests']
)
def download_photo(req_id: int = Query(ge=0), expert_service: ExpertService = Depends()):
    return expert_service.get_photo(req_id)


@router.patch(
    '/set_view_status',
    status_code=status.HTTP_200_OK,
    response_model=Optional[schemas.RequestExpertBase],
    tags=['expert requests'],
)
def set_view_status(req_id: int = Query(ge=0), session: Session = Depends(get_session)):
    return set_status(req_id, "view", session)


@router.patch(
    '/set_clean_status',
    status_code=status.HTTP_200_OK,
    response_model=Optional[schemas.RequestExpertBase],
    tags=['expert requests'],
)
def set_clean_status(req_id: int = Query(ge=0), session: Session = Depends(get_session)):
    return set_status(req_id, "clean", session)
