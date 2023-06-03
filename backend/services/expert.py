from fastapi import Depends

from database.db import Session, get_session


class Expert:
    def __init__(
            self,
            session: Session = Depends(get_session)
    ):
        self.session = session
