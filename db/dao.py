from sqlalchemy import text
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError
import datetime

from db.basic import db_session
from db.models import (
    MainUrl, WebInfo,SpiderTask
)
from decorators import db_commit_decorator


class MainUrlOper:


    @classmethod
    @db_commit_decorator
    def update_mainurl(cls, parameter):
        pid = parameter['pid']
        mainurl = db_session.query(MainUrl).filter(MainUrl.pid == pid).first()

        try:
            remark = parameter['remark']
            mainurl.remark = remark
            db_session.commit()
            db_session.close()
        except:
            pass
        try:
            status = parameter['status']
            mainurl.status = status
            db_session.commit()
            db_session.close()
        except:
            pass

        try:
            rule= parameter['rule']
            mainurl.rule =  rule
            db_session.commit()
            db_session.close()
        except:
            pass

    @classmethod
    @db_commit_decorator
    def delete_one(cls, parameter):
        maininfo = db_session.query(MainUrl).filter(
            MainUrl.pid == parameter["pid"]).first()
        db_session.delete(maininfo)
        db_session.commit()
        db_session.close()

    @classmethod
    @db_commit_decorator
    def add_one(cls, parameter):
        mainurl = MainUrl()
        mainurl.address = parameter['address']
        mainurl.webSite = parameter['webSite']
        mainurl.status = 0
        mainurl.remark = ""
        mainurl.sort = int(parameter['sort'])
        db_session.add(mainurl)
        db_session.commit()
        db_session.close()
        return mainurl.pid


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
            datas = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.status == status,
                                                     MainUrl.webSite.like(
                                                         "%{}%".format(keyword))).limit(
                        limit).offset(
                        (page - 1) * limit)
            count = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.status == status,
                                                     MainUrl.webSite.like("%{}%".format(keyword))).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data":[item.single_to_dict() for item in datas], "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}


class WebInfoOper:


    @classmethod
    @db_commit_decorator
    def add_one(cls, parameter):
        webinfo = WebInfo()
        webinfo.url = parameter['url']
        webinfo.add_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        webinfo.agent = int(parameter['agent'])
        webinfo.status = 0
        webinfo.web_name = parameter['web_name']
        webinfo.sort = int(parameter['sort'])
        webinfo.pid = int(parameter['pid'])
        db_session.add(webinfo)
        db_session.commit()
        db_session.close()
        return webinfo.id

    @classmethod
    @db_commit_decorator
    def delete_one(cls, parameter):
        webinfo = db_session.query(WebInfo).filter(
            WebInfo.id == parameter["id"]).first()
        db_session.delete(webinfo)
        db_session.commit()
        db_session.close()

    @classmethod
    @db_commit_decorator
    def update_webinfo(cls,parameter):

        id = parameter['id']
        webinfo = db_session.query(WebInfo).filter(WebInfo.id == id).first()
        try:
            remark = parameter['remark']
            webinfo.remark = remark
        except:
            status = parameter['status']
            webinfo.remark = status

        finally:
            db_session.commit()
            db_session.close()



    @classmethod
    def select_by_parameter(cls, parameter):


        page = int(parameter['page'])
        limit = int(parameter['limit'])
        pid = int(parameter['pid'])

        try:
            datas = db_session.query(WebInfo).filter(
                                             WebInfo.pid == pid).limit(limit).offset(
                (page - 1) * limit)
            count = db_session.query(WebInfo).filter(
                                                     WebInfo.pid == pid).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data": [item.json() for item in datas], "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

class SpiderTaskOper:


    @classmethod
    @db_commit_decorator
    def delete_one(cls, parameter):
        spider_task = db_session.query(SpiderTask).filter(
            SpiderTask.id == parameter["id"]).first()
        db_session.delete(spider_task)
        db_session.commit()
        db_session.close()

    @classmethod
    @db_commit_decorator
    def add_one(cls, parameter):

        spider_task = SpiderTask()
        spider_task.task_name = parameter['task_name']
        spider_task.create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        spider_task.status = 0
        spider_task.creater = 'admin'
        db_session.add(spider_task)
        db_session.commit()
        db_session.close()
        return spider_task.id

    @classmethod
    def select_by_parameter(cls, parameter):

        page = int(parameter['page'])
        limit = int(parameter['limit'])
        status = int(parameter['status'])
        keyword = str(parameter['keyword'])
        try:
            datas = db_session.query(SpiderTask).filter(SpiderTask.status == status,
                                                        SpiderTask.task_name.like(
                                                         "%{}%".format(keyword))).limit(
                        limit).offset(
                        (page - 1) * limit)
            count = db_session.query(SpiderTask).filter(SpiderTask.status == status,
                                                        SpiderTask.task_name.like("%{}%".format(keyword))).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data":[item.single_to_dict() for item in datas], "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

if __name__ == '__main__':
    import json
    # rule = json.dumps({
    #     'page': 10,
    #     'good_list': "//ul[@id= 'newsListContent']//li//p[@class='title']//a//@href",
    #     'domain': 'http://stock.eastmoney.com/a/cdpfx_{}.html',
    #     "content_xpath": {
    #         'personnel_title': '//h1//text()',
    #         'attendance_time': '//div[@class="time"]//text()',
    #     },
    #     'author': 'snail'})
    # parameter = {
    #     "pid": 5905,
    #     "rule":rule
    #
    # }
    #
    # spider = SpiderTaskOper()
    # parameter = {
    #         "page":1,
    #         "limit":10,
    #         "status":0,
    #         "keyword":""
    #     }
    # print(spider.select_by_parameter(parameter))
    #
    parameter = {"task_name":"test"}
        #     # spider.add_one(parameter)

