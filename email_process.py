import smtplib
import imaplib
from email.parser import BytesParser
from email.policy import default

class EmailWorker:
    def __init__(self, user_email, login, password, smtp_server, port=465):
        self.user_email = user_email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.port = port
        self.connection = None

    def connect(self):
        self.connection = smtplib.SMTP_SSL(self.smtp_server, self.port)
        self.connection.login(self.login, self.password)

    def disconnect(self):
        self.connection.quit()

    def send_email(self, to_address, subject, message):
        if not self.connection:
            self.connect()

        from_address = self.user_email
        headers = [
            f"From: {from_address}",
            f"To: {to_address}",
            f"Subject: {subject}",
            "MIME-Version: 1.0",
            "Content-Type: text/html"
        ]
        body = '\r\n'.join(headers) + '\r\n\r\n' + message
        self.connection.sendmail(from_address, to_address, body.encode('utf-8'))

    def read_emails(self):
        if not self.connection:
            self.connect()

        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.login, self.password)
            server.select('INBOX')
            status, data = server.search(None, 'ALL')
            email_ids = list(data[0].split())[::-1]


            emails = []
            for email_id in email_ids:
                status, data = server.fetch(email_id, '(RFC822)')
                email_data = data[0][1]
                parser = BytesParser(policy=default)
                email_message = parser.parsebytes(email_data)
                emails.append(email_message)
                if len(emails)==2:
                    break

        return emails
