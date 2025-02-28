from flask import current_app as app
from backend.celery.tasks import email_reminder

celery_app = app.extensions['celery']

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # every 10 seconds
    sender.add_periodic_task(10.0, email_reminder.s('students@gmail', 'reminder to login', '<h1> hello everyone </h1>') )

@celery_app.task
def task(arg):
    print(arg)