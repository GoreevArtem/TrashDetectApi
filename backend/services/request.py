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
        user = self.session.query(models.User).filter(models.User.id == self.user_id).first()

        user.requests.extend([models.Request(**new_request.dict())])

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return new_request

    def get_request(self, limit: int = 10) -> Optional[List[schemas.Request]]:
        try:
            return self.session.query(models.Request).filter(models.Request.user_id == self.user_id).limit(limit).all()
        except:
            return None
