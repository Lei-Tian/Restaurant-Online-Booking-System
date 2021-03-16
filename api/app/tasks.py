from celery.utils.log import get_task_logger
from app.core.celery_app import celery_app
from app.db.session import get_session
from app.db.models.restaurant import OrderStatus

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
