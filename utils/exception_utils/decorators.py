from functools import wraps

from db.basic import db_session


def db_commit_decorator(func):
    @wraps(func)
    def session_commit(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            db_session.rollback()
            return  {"code": "500", "message": '数据库服务异常'}
    return session_commit

def parse_text(func):
    @wraps(func)
    def filter_url(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('获取不到数据')
    return filter_url