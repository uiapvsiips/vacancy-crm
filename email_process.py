import imaplib
import poplib
import smtplib
from email import message_from_bytes
from email.parser import BytesParser
from email.policy import default


class EmailWorker:
    def __init__(self, user_email, login, password,smtp_server,smtp_port, pop_server,pop_port, imap_server, imap_port):
        self.user_email = user_email
        self.login = login
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.pop_server = pop_server
        self.pop_port = pop_port
        self.imap_server = imap_server
        self.imap_port = imap_port
        self.smtp_connection = None
        self.imap_pop_connection = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


    def connect(self, protocol):
        if protocol == 'smtp':
            self.smtp_connection = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            self.smtp_connection.login(self.login, self.password)
        else:
            if protocol=='pop':
                self.imap_pop_connection = poplib.POP3_SSL(self.pop_server, self.pop_port)
            elif protocol=='imap':
                self.imap_pop_connection = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            self.imap_pop_connection.login(self.login, self.password)

    def disconnect(self):
        if self.smtp_connection:
            self.smtp_connection.quit()
            self.smtp_connection = None
        if self.imap_pop_connection:
            self.imap_pop_connection.quit()
            self.imap_pop_connection = None

    def send_email(self, to_address, subject, message):
        self.smtp_connection = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        self.smtp_connection.login(self.login, self.password)
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
             return self.read_emails_pop3(num_messages)
        elif protocol == 'imap':
             return self.read_emails_imap(num_messages)
        else:
            raise ValueError('Unknown protocol')

    def read_emails_imap(self, num_messages):
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as server:
            server.login(self.login, self.password)
            server.select('INBOX')
            # status, data = server.search(None, 'ALL')
            # email_ids = list(data[0].split())[::-1]
            # emails = []
            # for email_id in num_messages:
            #     status, data = server.fetch(b'1', '(RFC822)')
            #     email_data = data[0][1]
            #     parser = BytesParser(policy=default)
            #     email_message = parser.parsebytes(email_data)
            #     emails.append(email_message)
            #     if len(emails) == 2:
            #         break
            # Конвертируем список id в строку
            id_string = ','.join(str(i) for i in num_messages)

            # Запрашиваем тела писем с указанными id
            status, data = server.fetch(id_string, '(RFC822)')

            # Обрабатываем данные
            emails = []
            for email_data in data:
                if isinstance(email_data, tuple):
                    email_message = BytesParser(policy=default).parsebytes(email_data[1])
                    emails.append(email_message)
        return emails

    def read_emails_pop3(self, num_messages, limit=10):
        self.imap_pop_connection = poplib.POP3_SSL(self.pop_server, self.pop_port)
        self.imap_pop_connection.user(self.login)
        self.imap_pop_connection.pass_(self.password)
        emails = []
        for num_message in num_messages:
            raw_email = b"\n".join(self.imap_pop_connection.retr(num_message)[1])
            email = message_from_bytes(raw_email)
            emails.append(email)
        return emails
