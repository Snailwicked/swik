# -*-coding:utf-8 -*-
from functools import wraps
from traceback import format_tb
from dbs.basic_db import db_session


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("数据更新异常")
            db_session.rollback()
    return session_commit