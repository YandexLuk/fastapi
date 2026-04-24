from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from core.config import settings


class Database:
    def __init__(self):
        self._engine = create_engine(settings.SQLITE_URL)

    @contextmanager
    def session(self):
        connection = self._engine.connect()

        Session = sessionmaker(bind=self._engine)
        session = Session()

        try:
            yield session
            session.commit()
            connection.close()
        except Exception:
            session.rollback()
            raise


database = Database()
Base = declarative_base()