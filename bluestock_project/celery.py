import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bluestock_project.settings')

app = Celery('bluestock_project')

# Read config from Django settings using a 'CELERY_' prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# --- SECTION 7.3 CELERY AUTOMATION SCHEDULE DEFINITIONS ---
app.conf.beat_schedule = {
    'run_etl_pipeline_daily': {
        'task': 'dashboard.tasks.run_automated_financial_pipeline', 
        'schedule': crontab(hour=1, minute=0),  # Daily 1:00 AM
    },
    'generate_audit_report_daily': {
        'task': 'dashboard.tasks.generate_daily_pipeline_report', # Linked to your reporting script!
        'schedule': crontab(hour=8, minute=0),  # Daily 8:00 AM
    },
    # --- Keep these linked to your primary analytics execution tasks as needed ---
    'score_all_companies_daily': {
        'task': 'dashboard.tasks.run_automated_financial_pipeline',
        'schedule': crontab(hour=2, minute=0),  # Daily 2:00 AM
    },
    'detect_anomalies_weekly': {
        'task': 'dashboard.tasks.run_automated_financial_pipeline',
        'schedule': crontab(hour=0, minute=0, day_of_week='sun'), # Weekly Sunday 12:00 AM
    },
}