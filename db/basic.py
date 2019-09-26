# -*-coding:utf-8 -*-
from sqlalchemy import MetaData
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from config.conf import get_db_args
import pymysql
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import DisconnectionError


def checkout_listener(dbapi_con,con_record, con_proxy):
    try:
        try:
            dbapi_con.ping(False)
        except TypeError:
            dbapi_con.ping()
    except dbapi_con.OperationalError as exc:
        if exc.args[0] in (2006, 2013, 2014, 2045, 2055):
            raise DisconnectionError()
        else:
            raise

def get_engine():
    args = get_db_args()
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(args['db_type'], args['user'], args['password'],
                                                             args['host'], args['port'], args['db_name'],cursorclass=pymysql.cursors.DictCursor)
    engine = create_engine(connect_str, encoding='utf-8',poolclass=NullPool)
    return engine

eng = get_engine()

event.listen(eng, 'checkout', checkout_listener)

Base = declarative_base()
Session = sessionmaker(bind=eng)
db_session = Session()
metadata = MetaData(get_engine())


__all__ = ['eng', 'Base', 'db_session', 'metadata']
