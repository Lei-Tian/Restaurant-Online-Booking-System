#!/usr/bin/env python3
import sys

sys.path.insert(0, ".")
from app.db.session import Base, SessionLocal, engine


def condition():
    while True:
        ans = input("Are you sure you want to clear all data?[Y/N]")
        if ans.strip().lower() == "y": return True
        if ans.strip().lower() == "n": return False


def execute():
    db = SessionLocal()
    Base.metadata.reflect(engine)
    print('Dropping all...')
    Base.metadata.drop_all(bind=engine)
    print('Creating all...')
    Base.metadata.create_all(bind=engine)
    print("Truncate complete!")


def main():
    if condition(): execute()


if __name__ == "__main__":
    main()
