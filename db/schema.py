from sqlalchemy import (Column, ForeignKey, Integer, String, BOOLEAN,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database


Base = declarative_base()

class ReceivedSms(Base):
    __tablename__ = 'received'
    id = Column(String(34), primary_key=True)
    from_num = Column(String(100), nullable=False)
    body = Column(String(1600), nullable=False)
    resolved = Column(BOOLEAN)

class Response(Base):
    __tablename__ = 'response'
    id = Column(Integer, primary_key=True)
    sms_id = Column(String(34), ForeignKey(ReceivedSms.__tablename__ + ".id"))
    to_num = Column(String(100), nullable=False)
    body = Column(String(1600), nullable=False)
    sent = Column(BOOLEAN)

class Endpoints(Base):
    __tablename__ = 'endpoints'
    id = Column(Integer, primary_key=True)
    grammar = Column(String(300), nullable=False)
    endpoint = Column(String(250), nullable=False)
    service = Column(String(100), nullable=False)


DB_NAME = 'twilio'
SQL_TYPE = 'mysql'
DRIVER = 'pymysql'
HOST = 'localhost'
USER = 'root'

def create_db_session(db_url=None):
    if db_url is None:
        db_url = generate_url()
    engine = create_engine(db_url)
    Base.metadata.bind = engine
    DBSession = sessionmaker(bind=engine)
    return DBSession()

def generate_url(db_name=DB_NAME, sql_type=SQL_TYPE, driver=DRIVER, host=HOST,
                 user=USER, password=None):
    if password:
        return '%s+%s://%s:%s@%s/%s' % (sql_type, driver, user, password,
                                        host, db_name)
    else:
        return '%s+%s://%s@%s/%s' % (sql_type, driver, user, host, db_name)

def create_tables(db_url=None):
    if db_url is None:
        db_url = generate_url()
    engine = create_engine(db_url)
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(create_engine(db_url))

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    arg = args[0]
    if arg == "create":
        if len(args) > 1:
            create_tables(args[1])
        else:
            create_tables()
