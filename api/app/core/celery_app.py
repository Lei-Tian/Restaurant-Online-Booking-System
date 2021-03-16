from celery import Celery

celery_app = Celery("worker", broker="redis://localhost", include=["app.tasks"])