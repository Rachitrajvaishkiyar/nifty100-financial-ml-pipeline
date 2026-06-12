import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluestock_project.settings')

app = Celery('dashboard')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# --- SECTION 7.3 STRICT BACKGROUND TASK CRONTABS ---
app.conf.beat_schedule = {
    'run_etl_pipeline_daily': {
        'task': 'dashboard.tasks.run_etl_pipeline',
        'schedule': crontab(hour=1, minute=0),  # Daily 1:00 AM
    },
    'score_all_companies_daily': {
        'task': 'dashboard.tasks.score_all_companies',
        'schedule': crontab(hour=2, minute=0),  # Daily 2:00 AM
    },
    'generate_pros_cons_daily': {
        'task': 'dashboard.tasks.generate_pros_cons',
        'schedule': crontab(hour=2, minute=30), # Daily 2:30 AM
    },
    'detect_anomalies_weekly': {
        'task': 'dashboard.tasks.detect_anomalies',
        'schedule': crontab(hour=0, minute=0, day_of_week='sun'), # Weekly Sunday
    },
    'detect_trends_weekly': {
        'task': 'dashboard.tasks.detect_trends',
        'schedule': crontab(hour=0, minute=0, day_of_week='sun'), # Weekly Sunday
    },
}