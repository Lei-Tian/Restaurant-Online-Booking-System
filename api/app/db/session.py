from fastapi import Request
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core import config

engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


@contextmanager
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency
def get_db(request: Request):
    db = SessionLocal()
    try:
        request.state.db = db
        yield db
    finally:
        db.close()
