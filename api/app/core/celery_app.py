from celery import Celery

from app.core.config import REDIS_URI

celery_app = Celery("worker", broker=REDIS_URI, include=["app.tasks"])

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.tasks import update_popular_restaurants
    interval_in_seconds = 60 * 5
    sender.add_periodic_task(
        interval_in_seconds,
        update_popular_restaurants.s(),
        name="periodic refresh popular restaurants"
    )

