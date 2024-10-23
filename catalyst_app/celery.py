# celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Replace with your project name

app = Celery('config')  # Replace with your project name
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
