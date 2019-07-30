from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError
import hashlib
import datetime

from db.basic import db_session
from db.models import (
    MainUrl, WebInfo
)
from decorators import db_commit_decorator


class MainUrlOper:


    # @classmethod
    # @db_commit_decorator
    # def add_all(cls, datas):
    #     try:
    #         db_session.add_all(datas)
    #         db_session.commit()
    #     except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
    #         for data in datas:
    #             cls.add_one(data)

    '''parameter = {'pid': 5905, 'sign': 'remark', 'content': '网站404'}'''
    @classmethod
    @db_commit_decorator
    def update_main_url(cls, parameter):
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

    '''
    parameter = {
            "page":1,
            "limit":10,
            "status":0,
            "sort":1,
            "keyword":""
        }
    '''
    @classmethod
    def select_by_parameter(cls, parameter):

        page = int(parameter['page'])
        limit = int(parameter['limit'])
        status = int(parameter['status'])
        keyword = str(parameter['keyword'])
        sort = int(parameter['sort'])
        try:
            data = [item.json() for item in
                    db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.status == status,
                                                     MainUrl.webSite.like(
                                                         "%{}%".format(keyword))).limit(
                        limit).offset(
                        (page - 1) * limit)]
            count = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.status == status,
                                                     MainUrl.webSite.like("%{}%".format(keyword))).count()
            return {"code": "200", "message": "succeed", "data": data, "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            return {"code": "404", "message": "fialed", "data": [], "count": 0}


class WebInfoOper:


    @classmethod
    @db_commit_decorator
    def add_one(cls, parameter):
        mainurl = MainUrl()
        mainurl.web_url = parameter['web_url']
        hl = hashlib.md5()
        hl.update(str(parameter['web_url']).encode("utf8"))
        mainurl.id = hl.hexdigest()
        mainurl.add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        mainurl.agent = int(parameter['agent'])
        mainurl.status = 0
        mainurl.web_name = parameter['web_name']
        mainurl.sort = int(parameter['sort'])
        mainurl.pid = int(parameter['pid'])
        db_session.add(mainurl)
        db_session.commit()


    @classmethod
    def select_by_parameter(cls, parameter):


        page = int(parameter['page'])
        limit = int(parameter['limit'])
        status = int(parameter['status'])
        checked = str(parameter['checked'])
        pid = int(parameter['pid'])
        try:
            data = [item.json() for item in
                    db_session.query(WebInfo).filter(WebInfo.checked == checked, WebInfo.status == status,
                                                     WebInfo.pid == pid).limit(limit).offset(
                        (page - 1) * limit)]
            count = db_session.query(WebInfo).filter(WebInfo.checked == checked, WebInfo.status == status,
                                                     WebInfo.pid == pid).count()
            return {"code": "200", "message": "succeed", "data": data, "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            return {"code": "404", "message": "fialed", "data": [], "count": 0}





