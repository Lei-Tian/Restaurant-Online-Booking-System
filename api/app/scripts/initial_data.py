#!/usr/bin/env python3
import sys

sys.path.insert(0, ".")

import csv
import logging
from functools import wraps

from app.db.crud.user import create_user
from app.db.models.location import Location
from app.db.models.restaurant import (
    Restaurant,
    RestaurantTable,
    RestaurantTableType,
    TableAvailability,
)
from app.db.schemas.user import UserCreate
from app.db.session import SessionLocal

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(name)s %(levelname)s:%(message)s')
logger = logging.getLogger(__file__)


def db_session(executor):
    @wraps(executor)
    def wrapper():
        db = SessionLocal()
        try:
            executor(db)
        finally:
            db.close()
    return wrapper


def load_data_from_file(filename):
    with open(f'../data/{filename}') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader, start=1):
            yield i, row


def bulk_insert(db, cls, filename, row_processor=None, batch=10000):
    rows = []
    for index, row in load_data_from_file(filename):
        if row_processor: row = row_processor(row)
        rows.append(row)
        if index % batch == 0:
            db.bulk_insert_mappings(cls, rows)
            db.commit()
            rows.clear()
            logger.debug(f"{filename}: {index} rows have been committed")
    db.bulk_insert_mappings(cls, rows)
    db.commit()


@db_session
def load_user(db):
    create_user(
        db,
        UserCreate(
            username="demo",
            password="demo",
            email="demo@gmail.com",
            is_active=True,
            is_superuser=True,
        ),
    )


@db_session
def load_location(db):
    bulk_insert(db, Location, 'location.csv')
    

@db_session
def load_restaurant(db):
    def row_processor(row):
        row['is_open'] = bool(int(row['is_open']))
        row['good_for_kids'] = True if row['good_for_kids'] == 'TRUE' else False
        return row
    bulk_insert(db, Restaurant, 'restaurant.csv', row_processor=row_processor)


@db_session
def load_restaurant_table(db):
    def row_processor(row):
        row['type'] = RestaurantTableType(row['type'])
        return row
    bulk_insert(db, RestaurantTable, 'restaurant_table_onlyopen.csv', row_processor=row_processor)


@db_session
def load_table_availability(db):
    def row_processor(row):
        row['is_available'] = True
        row['order_id'] = None
        return row
    bulk_insert(db, TableAvailability, 'table_availability.csv', row_processor=row_processor, batch=100000)


def init():
    for executor in [
        load_user,
        load_location,
        load_restaurant,
        load_restaurant_table,
        load_table_availability,
    ]:
        logger.info(f"executing {executor.__name__}...")
        executor()
        logger.info(f"{executor.__name__} is complete!")


if __name__ == "__main__":
    init()
