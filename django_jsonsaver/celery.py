import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_jsonsaver.settings')

# set the default Django settings module for the 'celery' program.
app = Celery('django_jsonsaver')


# periodic tasks
# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(
#         5.0, hello_periodic_task.s(), name='hello every 10')

# @app.task
# def hello_periodic_task():
#     print('hello')


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
