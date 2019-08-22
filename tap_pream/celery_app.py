from celery import Celery

from secret import redis_broker_url


app = Celery(
    broker=redis_broker_url,
    include=["tasks"]
)

