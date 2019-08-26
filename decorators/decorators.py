from functools import wraps

from db.basic import db_session


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            db_session.rollback()
            print('DB operation error，here are details:{}'.format(e))
    return session_commit


def parse_text(func):
    @wraps(func)
    def filter_url(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('获取不到数据')
    return filter_url