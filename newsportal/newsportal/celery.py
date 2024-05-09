import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsportal.settings')

app = Celery('newsportal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_weekly_posts_emails': {
        'task': 'news.tasks.send_weekly_posts_notification',
        'schedule': crontab(day_of_week='monday', hour='8', minute='0')
        # 'schedule': crontab(day_of_week='thursday', hour='18', minute='15')
        # 'schedule': crontab()
    },
}
# app.conf.timezone = 'Asia/Yekaterinburg'
app.conf.timezone = 'UTC'

