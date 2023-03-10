import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DB_HOST = os.environ.get('DB_HOST', 'localhost')
engine = create_engine(f'postgresql://postgres:pgpass@{DB_HOST}:5432/postgres')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def row2dict(row):
    result = {}
    for column in row.__table__.columns:
        result[column.name] = getattr(row, column.name)
    return result
