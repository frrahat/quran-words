from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.config import CONFIG


class SessionMakerMixin:
    __db_filename__ = ""

    @classmethod
    def get_session(cls):
        engine = create_engine(
            url=f"sqlite:///app/databases/{cls.__db_filename__}",
            connect_args={
                "check_same_thread": False,
            },
            echo=CONFIG.ECHO_SQL,
        )

        return Session(engine)
