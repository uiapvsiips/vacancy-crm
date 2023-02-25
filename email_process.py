import imaplib
import poplib
import smtplib
from email import message_from_bytes
from email.parser import BytesParser
from email.policy import default


class EmailWorker:
    def __init__(self, user_email, login, password, pop3_server, imap_server, smtp_server, pop3_port=995, imap_port=993, smtp_port=465):
        self.user_email = user_email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.pop3_server = pop3_server
        self.pop3_port = pop3_port
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.smtp_connection = None
        self.pop_connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    def connect(self, protocol='imap'):
        if protocol == 'imap':
            self.smtp_connection = smtplib.SMTP_SSL(self.smtp_server, self.port)
            self.smtp_connection.login(self.login, self.password)
            return
        self.pop_connection = poplib.POP3_SSL(self.pop, self.port)
        self.pop_connection.user(self.login)
        self.pop_connection.pass_(self.password)

    def disconnect(self):
        if self.smtp_connection:
            self.smtp_connection.quit()
            self.smtp_connection = None
        if self.pop_connection:
            self.pop_connection.quit()
            self.pop_connection = None;

    def send_email(self, to_address, subject, message):
        if not self.smtp_connection:
            self.connect(protocol='imap')
        from_address = self.user_email
        headers = [
            f"From: {from_address}",
            f"To: {to_address}",
            f"Subject: {subject}",
            "MIME-Version: 1.0",
            "Content-Type: text/html"
        ]
        body = '\r\n'.join(headers) + '\r\n\r\n' + message
        self.smtp_connection.sendmail(from_address, to_address, body.encode('utf-8'))

    def get_emails(self, num_messages, protocol):
        if protocol == 'pop3':
            self.read_emails_pop3(num_messages)
        elif protocol == 'imap':
            self.read_emails_smtp(num_messages)
        else:
            raise ValueError('Unknown protocol')

    def read_emails_smtp(self, num_messages):
        if not self.smtp_connection:
            self.connect(protocol='imap')

        with imaplib.IMAP4_SSL(self.smtp_server) as server:
            server.login(self.login, self.password)
            server.select('INBOX')
            status, data = server.search(None, 'ALL')
            # email_ids = list(data[0].split())[::-1]

            emails = []
            for email_id in num_messages:
                status, data = server.fetch(email_id, '(RFC822)')
                email_data = data[0][1]
                parser = BytesParser(policy=default)
                email_message = parser.parsebytes(email_data)
                emails.append(email_message)
                if len(emails) == 2:
                    break

        return emails

    def read_emails_pop3(self, num_messages, limit=10):
        emails = []
        if not self.pop_connection:
            self.connect(protocol='pop3')
        for i in range(num_messages, num_messages - limit, -1):
            raw_email = b"\n".join(self.pop_connection.retr(i)[1])
            email = message_from_bytes(raw_email)
            emails.append(email)
        return emails
