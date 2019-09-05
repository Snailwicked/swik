# -*-coding:utf-8 -*-
from sqlalchemy import create_engine, MetaData
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config.conf import get_db_args
import pymysql

def get_engine():
    args = get_db_args()
    connect_str = "{}+pymysql://{}:{}@{}:{}/{}?charset=utf8".format(args['db_type'], args['user'], args['password'],
                                                             args['host'], args['port'], args['db_name'],cursorclass=pymysql.cursors.DictCursor)
    engine = create_engine(connect_str, encoding='utf-8',poolclass=NullPool)
    return engine

eng = get_engine()
Base = declarative_base()
Session = sessionmaker(bind=eng)
db_session = Session()
metadata = MetaData(get_engine())


__all__ = ['eng', 'Base', 'db_session', 'metadata']
