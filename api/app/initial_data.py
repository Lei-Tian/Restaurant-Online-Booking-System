#!/usr/bin/env python3
import sys

sys.path.insert(0, ".")

from app.db.crud.user import create_user
from app.db.schemas.user import UserCreate
from app.db.session import SessionLocal


def init() -> None:
    db = SessionLocal()

    create_user(
        db,
        UserCreate(
            username="test",
            password="test",
            email="test@gmail.com",
            is_active=True,
            is_superuser=True,
        ),
    )


if __name__ == "__main__":
    print("Creating superuser test")
    init()
    print("Superuser created")