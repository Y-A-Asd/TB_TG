import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TB_TG.settings.dev')

celery = Celery('TB_TG')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
