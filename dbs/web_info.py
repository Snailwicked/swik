# -*-coding:utf-8 -*-
from dbs.basic_db import db_session
from dbs.models import WebInfo
from decorators.decorator import db_commit_decorator

'''
page=1&limit=10&pid=5930&status=1&checked=1
parameter = {
        "page":1,
        "limit":10,
        "status":0,
        "checked":1,
        "pid":5930
    }
'''
def select_web_info(parameter):
    page = int(parameter['page'])
    limit = int(parameter['limit'])
    status = int(parameter['status'])
    checked = str(parameter['checked'])
    pid = int(parameter['pid'])

    data = [item.json() for item in db_session.query(WebInfo).filter(WebInfo.checked == checked, WebInfo.status == status,
                        WebInfo.pid==pid).limit(limit).offset(
        (page - 1) * limit)]
    count = db_session.query(WebInfo).filter(WebInfo.checked == checked, WebInfo.status == status,
                        WebInfo.pid==pid).count()
    return {"code":"200","message":"succeed","data":data,"count":count}


'''
    data = {'id': 0af0ba3cbd3f8576f890c5623aee2e5f, 'sign': 'remark', 'content': '网站404'}

'''
@db_commit_decorator
def update_main_url(parameter):
    id = parameter['id']
    sign = parameter['sign']
    content = parameter['content']

    webinfo = db_session.query(WebInfo).filter(WebInfo.id == id).first()
    if sign == "remark":
        webinfo.remark = content
        db_session.commit()

    elif sign == "status":
        webinfo.status = content
        db_session.commit()



if __name__ == '__main__':
    parameter = {
        "page":1,
        "limit":10,
        "status":0,
        "checked":0,
        "pid":5930
    }

    print(select_web_info(parameter))
