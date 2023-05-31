from datetime import datetime

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
    ):
        _request = models.Request(**new_request.dict())
        _request.request_date = datetime.now()
        _request.user_id = self.user_id

        self.session.add(_request)
        self.session.commit()
        self.session.refresh(_request)

        return _request
