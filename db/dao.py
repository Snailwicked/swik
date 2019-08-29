from config import *
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError
import datetime,json

from db.basic import db_session
from db.models import (
    MainUrl,SpiderTask
)
from utils.exception_utils import db_commit_decorator


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
        mainurl.sort = 0
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


class SpiderTaskOper:

    def __int__(self):
        pass

    @classmethod
    @db_commit_decorator
    def start_task(cls, parameter):
        spider_name = int(parameter['id'])
        spider_task = db_session.query(SpiderTask).filter(
            SpiderTask.id == spider_name).first()
        spider_task.status = 1
        db_session.commit()
        datas = db_session.query(MainUrl).filter(MainUrl.spider_name == spider_name, MainUrl.status == 1).all()
        db_session.close()
        parameters = []
        for item in [item.single_to_dict() for item in datas]:
            parameter = {}
            url = item.get("address")
            if item["rule"] == None:
                crawler_info.info("{} : has no filtering rules, default algorithm acquisition".format(url))
                parameter["rule"] = {'filter_rule': '', 'page_size': '1', 'header': '', 'author': '', 'issueTime': '', 'content': ''}
            else:
                rule = item["rule"]
                filter_rule =json.loads(rule)["filter_rule"]
                if filter_rule and filter_rule!="":
                    rule = json.loads(item["rule"].replace("@","+"))
                    parameter["rule"] = rule
            parameter["url"] = url
            parameters.append(parameter)
        return parameters


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
        keyword = str(parameter['keyword'])
        try:
            datas = db_session.query(SpiderTask).filter(SpiderTask.task_name.like(
                                                         "%{}%".format(keyword))).limit(
                        limit).offset(
                        (page - 1) * limit)
            count = db_session.query(SpiderTask).filter(SpiderTask.task_name.like("%{}%".format(keyword))).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data":[item.single_to_dict() for item in datas], "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}



class TaskConfigOper:

    @classmethod
    def select_by_id(cls, parameter):

        spider_name = int(parameter['id'])

        try:
            datas = db_session.query(MainUrl).filter(MainUrl.spider_name == spider_name,MainUrl.status==1).all()
            count = db_session.query(MainUrl).filter(MainUrl.spider_name == spider_name,MainUrl.status==1).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data":[item.single_to_dict() for item in datas], "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    @classmethod
    def select_all(cls, parameter):

        page = int(parameter['page'])
        limit = int(parameter['limit'])
        sort = int(parameter['sort'])


        try:
            datas = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.spider_name == 0,MainUrl.status==1).limit(
                        limit).offset(
                        (page - 1) * limit)
            count = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.spider_name == 0,MainUrl.status==1).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data":[item.single_to_dict() for item in datas], "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    @classmethod
    @db_commit_decorator
    def update_task_name(cls, parameter):

        spider_name = int(parameter['task_id'])
        main_url_pids = eval(parameter['main_url_pids'])
        main_url_remove_pids = eval(parameter['main_url_remove_pids'])
        try:
            for main_url_pid in main_url_pids:
                main_url = db_session.query(MainUrl).filter(
                    MainUrl.pid == main_url_pid).first()
                main_url.spider_name = spider_name
                
            for main_url_pid in main_url_remove_pids:
                main_url = db_session.query(MainUrl).filter(
                    MainUrl.pid == main_url_pid).first()
                main_url.spider_name = 0

            db_session.commit()
            db_session.close()
            return {"code": "200", "message": "更新成功"}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "更新失败"}



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
    spider = TaskConfigOper()
    # parameter = {
    #         "page":2,
    #         "limit":10,
    #         "sort":0
    #     }
    # print(spider.select_all(parameter))
    parameter = {
            "id":1
        }
    print(spider.select_by_id(parameter))
        #     # spider.add_one(parameter)

