from celery import Celery
from email_process import EmailWorker
import os

CELERY_HOST = os.getenv('CELERY_HOST', 'localhost')
app = Celery('tasks', broker=f'amqp://guest@{CELERY_HOST}//')

@app.task
def send_email(email_creds, subject, message, recipient):
    with EmailWorker(email_creds.email, email_creds.login, email_creds.password,
                     email_creds.smtp_server, email_creds.smtp_port,
                     email_creds.pop3_server, email_creds.pop3_port,
                     email_creds.imap_server, email_creds.imap_port) as email:
        email.send_email(recipient, subject, message)