import json

from celery.utils.log import get_task_logger

from app.core.celery_app import celery_app
from app.db.models.restaurant import OrderStatus
from app.db.session import get_session
from app.utils import constants
from app.utils.cache import redis_client
from app.utils.crud import get_all_locations

logger = get_task_logger(__name__)


@celery_app.task(acks_late=True)
def greeting(words: str):
    logger.info(words)


@celery_app.task(acks_late=True)
def cancel_order(order_ref_id: str):
    logger.info(f"Cancelling order(ref_id={order_ref_id})")
    with get_session() as db:
        db.execute(f"UPDATE order SET status = {OrderStatus.cancelled.value} WHERE ref_id = {order_ref_id}")
    logger.info(f"Order(id={order_ref_id}) has been cancelled")


@celery_app.task
def update_popular_restaurants():
    logger.info("refreshing popular restaurants...")
    with get_session() as db:
        for location in get_all_locations():
            location_id = location['id']
            key = f"{constants.POPULAR_RESTAURANTS_PER_LOCATION_PREFIX}{location_id}"
            logger.info(f"updating popular restaurants(key={key}) to cache...")
            rows = db.execute(f"SELECT id FROM restaurant where is_open = true AND location_id = {location_id} ORDER BY star DESC").fetchall()
            restaurant_ids = [row[0] for row in rows]
            redis_client.set(key, json.dumps(restaurant_ids),  60 * 60)
            logger.info(f"updated restaurants with count={len(restaurant_ids)}")
    logger.info(f"update popular restaurants is complete!")
