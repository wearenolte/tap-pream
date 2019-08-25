from celery import Celery

from secret import redis_broker_url


app = Celery(
    broker=redis_broker_url,
    backend=redis_broker_url,
    include=["tasks"],
)

app.conf.beat_schedule = {
    "test-beat": {
        "task": "tasks.test_task_flow",
        "schedule": 30.0,
    },
}

app.conf.timezone = "UTC"
