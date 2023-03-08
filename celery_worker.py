from celery import Celery
from email_process import EmailWorker
import os

RABBIT_HOST = os.getenv('RABBIT_HOST', 'localhost')
app = Celery('tasks', broker=f'amqp://guest@{RABBIT_HOST}//')


@app.task
def send_email(email_creds, subject, message, recipient):
    email = EmailWorker(**email_creds)
    email.send_email(recipient, subject, message)
