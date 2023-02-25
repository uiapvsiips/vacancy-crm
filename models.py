from sqlalchemy import Column, Integer, String, ForeignKey, func, Text, text
from alchemy_db import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class EmailCredentials(Base):
    __tablename__ = 'email_creds'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    email = Column(String(120), unique=True, nullable=False)
    login = Column(String(120), unique=True, nullable=False)
    password = Column(String(120), nullable=False)
    smtp_server = Column(String(120), nullable=False)
    smtp_port = Column(Integer, nullable=False)
    pop_server = Column(String(120))
    pop_port = Column(Integer)
    imap_server = Column(String(120))
    imap_port = Column(Integer)


    def __init__(self, login, password, email, smtp_server, smtp_port, pop_server, pop_port, imap_server, imap_port):
        self.login = login
        self.password = password
        self.email = email
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.pop_server = pop_server
        self.pop_port = pop_port
        self.imap_server = imap_server
        self.imap_port = imap_port


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    creation_date = Column(String(25), nullable=False, server_default=text("date_trunc('second', now())"))
    status = Column(Integer, nullable=False, default=0)
    position_name = Column(String(120), nullable=False)
    company = Column(String(120), nullable=False)
    description = Column(String(5000), nullable=False)
    contacts_ids = Column(String(120), nullable=False)
    comment = Column(String(120))
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, postion_name, company, description, contacts_ids, user_id, status = 0, comment=None):
        self.position_name = postion_name
        self.company = company
        self.description = description
        self.contacts_ids = contacts_ids
        self.comment = comment
        self.status = status
        self.user_id = user_id

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, primary_key=True, autoincrement=True)
    vacancy_id = Column(Integer,ForeignKey('vacancy.id'), nullable=False)
    description = Column(String(1000), nullable=False)
    event_date = Column(String(20), nullable=False, server_default=func.now())
    title = Column(String(120), nullable=False)
    due_to_date = Column(String(20), nullable=False)
    status = Column(Integer, nullable=False, default=0)

    def __init__(self, vacancy_id, description, title, due_to_date, status=0):
        self.description = description
        self.title = title
        self.due_to_date = due_to_date
        self.vacancy_id = vacancy_id
        self.status = status


class Template(Base):
    __tablename__ = 'templates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))

    def __init__(self, name, content, user_id):
        self.name = name
        self.content = content
        self.user_id = user_id
