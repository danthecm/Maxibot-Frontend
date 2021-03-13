web: gunicorn app:app
worker: celery -A  app.celery worker --loglevel=info
celery_beat: celery -A app.celery beat -l info