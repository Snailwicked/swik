# -*-coding:utf-8 -*-
from db.basic import db_session
from db.models import MainUrl


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
    parameter = {
        "page":1,
        "limit":10,
        "status":0,
        "sort":0,
        "keyword":"法制周末"
    }

    print(select_main_url(parameter))
