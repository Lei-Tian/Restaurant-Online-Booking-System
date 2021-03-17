from celery import Celery

celery_app = Celery("worker", broker="redis://localhost", include=["app.tasks"])

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    from app.tasks import update_popular_restaurants
    interval_in_seconds = 5
    sender.add_periodic_task(
        interval_in_seconds,
        update_popular_restaurants.s(),
        name="periodic refresh popular restaurants"
    )

