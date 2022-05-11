# pylint: disable=attribute-defined-outside-init
from __future__ import annotations

import abc

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from app.config.database import SessionLocal
from app.core.repositories.user import UserRepository



#models.Base.metadata.create_all(bind=engine)

class AbstractUnitOfWork(abc.ABC):
   
    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=SessionLocal):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.users = UserRepository(self.session)

        return super().__enter__()

    def __exit__(self, *args):
        self.session.close()
        super().__exit__(*args)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
