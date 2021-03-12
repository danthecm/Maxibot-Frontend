web: gunicorn app:app
worker: app.celery celery worker --loglevel=info
celery_beat: app.celery celery beat --loglevel=info