import json
import typing as t

from celery.utils.log import get_task_logger
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import Base, get_session
from app.utils import constants
from app.utils.cache import redis_client

logger = get_task_logger(__name__)


def get_all_items(db: Session, model: Base, skip: int = 0, limit: int = 100):
    return db.query(model).offset(offset=skip).limit(limit).all()


def get_item(db: Session, model: Base, _id: int):
    item = db.query(model).filter(model.id == _id).first()
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f"id={_id} is not found in {model.__tablename__}",
        )
    return item


def get_item_by_name(db: Session, model: Base, name: str):
    return db.query(model).first(model.name == name)


def create_item(db: Session, model: Base, payload: t.Union[dict, BaseModel]):
    if isinstance(payload, BaseModel): payload = payload.dict()
    db_item = model(**payload)
    db.add(db_item)
    db.commit()
    return db_item


def update_item(db: Session, model: Base, _id: int, payload: t.Union[dict, BaseModel]):
    db_item = get_item(db, model, _id)
    update_data = payload.dict(exclude_unset=True) if isinstance(payload, BaseModel) else payload
    for k, v in update_data.items():
        setattr(db_item, k, v)
    db.commit()
    return db_item


def delete_item(db: Session, model: Base, _id: int):
    db_item = get_item(db, model, _id)
    db.delete(db_item)
    db.commit()
    return db_item


def get_all_locations() -> t.List[dict]:
    locations = redis_client.get(constants.ALL_LOCATIONS)
    if locations:
        logger.info("locations are loaded from cache")
        locations = json.loads(locations)
    else:
        locations = []
        with get_session() as db:
            rows = db.execute(f"SELECT * FROM all_open_locations").fetchall()
            logger.info("locations are loaded from db")
            for _id, city, state, country in rows:
                locations.append({"id": _id, "city": city, "state": state, "country": country})
            redis_client.set(constants.ALL_LOCATIONS, json.dumps(locations), 60 * 60)
            logger.info("locations are set to cache")
    return locations


def get_popular_restaurants(location_id: int) -> t.List[int]:
    key = f"{constants.POPULAR_RESTAURANTS_PER_LOCATION_PREFIX}{location_id}"
    ret = redis_client.get(key)
    logger.info(f"popular restaurants(key={key}) are loaded from cache")
    return json.loads(ret) if ret else []
