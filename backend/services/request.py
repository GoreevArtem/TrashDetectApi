from datetime import datetime

from typing import List, Optional
from fastapi import Depends

from database import models
from schemas import schemas
from database.db import Session, get_session
from utils import oauth2


class RequestService:
    def __init__(
            self,
            session: Session = Depends(get_session),
            user_id: int = Depends(oauth2.require_user)
    ):
        self.session = session
        self.user_id = user_id

    def create_new_request(
            self,
            new_request: schemas.CreateRequest
    ) -> schemas.CreateRequest:
        new_request = models.Request(**new_request.dict())
        new_request.request_date = datetime.now()
        new_request.user_id = self.user_id

        self.session.add(new_request)
        self.session.commit()
        self.session.refresh(new_request)

        return new_request

    def get_request(self, limit: int = 10) -> Optional[List[schemas.Request]]:
        try:
            return self.session.query(models.Request).filter(models.Request.user_id == self.user_id).limit(limit).all()
        except:
            return None
