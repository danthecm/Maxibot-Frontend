web: gunicorn app:app
worker: celery -A app.celery worker -l INFO
worker: celery -A app.celery beat -l INFO