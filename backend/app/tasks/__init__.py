from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "bank_statements",
    broker=settings.redis_url,
    backend=settings.redis_url,
)
celery_app.conf.update(
    task_track_started=True,
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    worker_prefetch_multiplier=1,
    worker_pool='asyncio',
)
celery_app.autodiscover_tasks(['app.tasks'])
