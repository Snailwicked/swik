# -*-coding:utf-8 -*-
from dbs.basic_db import db_session
from dbs.models import MainUrl
from decorators.decorator import db_commit_decorator

'''
parameter = {
        "page":1,
        "limit":10,
        "status":0,
        "sort":1,
        "keyword":"扬州"
    }
'''
def select_main_url(parameter):
    page = int(parameter['page'])
    limit = int(parameter['limit'])
    status = int(parameter['status'])
    keyword = str(parameter['keyword'])
    sort = int(parameter['sort'])

    data = [item.json() for item in db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.status == status,
                                     MainUrl.webSite.like("%{}%".format(keyword))).limit(limit).offset(
        (page - 1) * limit)]
    count = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.status == status,
                                     MainUrl.webSite.like("%{}%".format(keyword))).count()
    return {"code":"200","message":"succeed","data":data,"count":count}


'''
    data = {'pid': 5905, 'sign': 'remark', 'content': '网站404'}

'''
@db_commit_decorator
def update_main_url(parameter):
    pid = parameter['pid']
    sign = parameter['sign']
    content = parameter['content']

    mainurl = db_session.query(MainUrl).filter(MainUrl.pid == pid).first()
    if sign == "remark":
        mainurl.remark = content
        db_session.commit()

    elif sign == "status":
        mainurl.status = content
        db_session.commit()



if __name__ == '__main__':
    parameter = {'pid': 5905, 'sign': 'status', 'content': 0}

    print(update_main_url(parameter))
