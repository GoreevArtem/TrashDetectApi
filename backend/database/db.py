from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings.settings import settings

DATABASE_URL: str = \
    f"postgresql://{settings.postgres_user}:{settings.postgres_password}@db:5432/{settings.postgres_db}"

engine = create_engine(
    DATABASE_URL
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session() -> Generator:
    with Session() as session:
        yield session
