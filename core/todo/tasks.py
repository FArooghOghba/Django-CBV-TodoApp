from celery.schedules import crontab

from .models import Task
from core.celery import app as celery_app


@celery_app.task
def delete_complete_tasks():
    tasks = Task.objects.filter(complete=True).delete()
    print(tasks)


@celery_app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='*/10'),
        delete_complete_tasks.s(),
        name='deleting complete tasks every 10 min.'
    )

# celery -A core beat -l info