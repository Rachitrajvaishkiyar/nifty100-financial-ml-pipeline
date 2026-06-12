web: gunicorn bluestock_project.wsgi:application
worker: celery -A bluestock_project worker --loglevel=info
beat: celery -A bluestock_project beat --loglevel=info