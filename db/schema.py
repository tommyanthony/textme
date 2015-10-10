from sqlalchemy import (Column, ForeignKey, Integer, DECIMAL, String, BOOLEAN,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker


Base = declarative_base()

class RecievedSms(Base):
    __tablename__ = 'recieved'
    id = Column(String(34), primary_key=True)
    from_num = Column(String(100), nullable=False)
    body = Column(String(1600), nullable=False)
    resolved = Column(BOOLEAN)

class Response(Base):
    id = Column(Integer, primary_key=True)
    sms_id = Column(Integer, ForeignKey(RecievedSms.__tablename__ + ".id"))
    to_num = Column(String(100), nullable=False)
    body = Column(String(1600), nullable=False)
    sent = Column(BOOLEAN)

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
    Base.metadata.create_all(create_engine(db_url))
