from celery import Celery
from email_process import EmailWorker
from models import EmailCredentials
import os

CELERY_HOST = os.getenv('CELERY_HOST', 'localhost')
app = Celery('tasks', broker=f'amqp://guest@{CELERY_HOST}//')


@app.task
def send_email(email_creds: EmailCredentials, subject, message, recipient):
    email = EmailWorker(email_creds.email, email_creds.login, email_creds.password,
                        email_creds.smtp_server, email_creds.smtp_port,
                        email_creds.pop_server, email_creds.pop_port,
                        email_creds.imap_server, email_creds.imap_port)
    email.send_email(recipient, subject, message)
