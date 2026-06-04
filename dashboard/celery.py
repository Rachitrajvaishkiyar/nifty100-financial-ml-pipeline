import os
from celery import Celery

# Set default Django settings module for celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluestock_project.settings')

app = Celery('bluestock_project')

# Read config from Django settings using a 'CELERY_' prefix
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')