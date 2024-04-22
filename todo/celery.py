# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from celery.schedules import crontab
# from celery import Celery
# from django.conf import settings
# from celery.schedules import crontab


# # Set the DJANGO_SETTINGS_MODULE environment variable
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

# # Create the Celery application
# app = Celery('todo')

# app.config_from_object(settings, namespace='CELERY')



# # app.conf.beat_schedule = {
  
# #     'auto_review_email':{
# #         'task': 'apps.review.tasks.auto_review_email',
# #         # 'schedule' : crontab(hour=12, minute=44),
# #         'schedule': crontab(hour=11, minute=0)
# #         # 'args':
# #     },
# # }
# from celery.schedules import crontab

# app.conf.beat_schedule = {
#     'auto_review_email': {
#         'task': 'apps.review.tasks.auto_review_email',
#         'schedule': crontab(minute='*/5'),  # Run every 5 minutes
#     },
# }


# app.autodiscover_tasks()

# # app.conf.enable_utc = True








# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request : {self.request!r}')
