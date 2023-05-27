from fastapi import APIRouter, status
from fastapi import Depends

from database import models
from database.db import Session, get_session
from schemas import schemas
from utils import oauth2

router = APIRouter(
    prefix='/user',
    tags=['user'],
)


def get_user_by_id(db: Session = Depends(get_session), user_id: str = Depends(oauth2.require_user)):
    return db.query(models.User).filter(models.User.id == user_id).first()


@router.get('/me', response_model=schemas.UserResponse)
# @cache(expire=60)
def get_me(db: Session = Depends(get_session), user_id: str = Depends(oauth2.require_user)):
    return get_user_by_id(db, user_id)


@router.delete('/me_delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_me(db: Session = Depends(get_session), user_id: str = Depends(oauth2.require_user)):
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
