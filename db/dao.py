from config import *
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError
from sqlalchemy.exc import InvalidRequestError
import datetime, json
import time

from db.basic import db_session
from db.models import (
    MainUrl, SpiderTask, KeyWords, WordList, Template, KeyAndTemplate
)
from utils.exception_utils import db_commit_decorator


class KeyWordsOper:

    @classmethod
    @db_commit_decorator
    def select_by_parameter(cls, parameter):

        page = int(parameter['page'])
        limit = int(parameter['limit'])
        try:
            datas = db_session.query(KeyWords).limit(
                limit).offset(
                (page - 1) * limit)
            count = db_session.query(KeyWords).count()

            db_session.close()
            info_list = []
            for item in datas:
                new_item = item.single_to_dict()
                new_item["key_words_list"] = [{"key": "微博", "words_list": ["信用卡", "刷单"]},
                                              {"key": "知乎", "words_list": ["贷款", "信贷"]}]
                info_list.append(new_item)
            return {"code": "200", "message": "succeed", "data": info_list,
                    "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    @classmethod
    @db_commit_decorator
    def select_by_id(cls, parameter):

        id = int(parameter['id'])
        try:
            KeyWords_info = db_session.query(KeyWords).filter(KeyWords.id == id).first()
            new_key_info = KeyWords_info.single_to_dict()
            KeyAndTemplate_info = db_session.query(KeyAndTemplate).filter(KeyAndTemplate.key_id == id)
            word_list = []
            for item in KeyAndTemplate_info:
                item_info = {}
                Template_info = db_session.query(Template).filter(
                    Template.id == int(item.single_to_dict()["template_id"])).first()
                WordList_info = db_session.query(WordList).filter(
                    WordList.id == int(item.single_to_dict()["word_list_id"])).first()
                item_info["id"] = WordList_info.single_to_dict()["id"]
                item_info["key"] = Template_info.single_to_dict()["template_name"]
                item_info["key_id"] = Template_info.single_to_dict()["id"]

                item_info["word_list"] = str(WordList_info.single_to_dict()["word_list"]).split(",")
                item_info["pid"] = Template_info.single_to_dict()["id"]
                word_list.append(item_info)
            new_key_info["word_list"] = word_list

            db_session.close()

            return {"code": "200", "message": "succeed", "data": new_key_info,
                    "count": 1}
        #
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    @classmethod
    @db_commit_decorator
    def delete_by_id(cls, parameter):

        id = int(parameter['id'])
        try:
            result = cls.select_by_id(parameter)
        except:
            return {"code": "404", "message": "数据库异常"}
        if result["data"]["word_list"]:
            return {"code": "400", "message": "请先清空关键词中所有词组"}
        else:
            try:
                keyword = db_session.query(KeyWords).filter(
                    KeyWords.id == id).first()
                db_session.delete(keyword)
                db_session.commit()
                db_session.close()
                return {"code": "200", "message": "删除成功"}
            except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
                db_session.close()

    @classmethod
    @db_commit_decorator
    def add_key_word(cls, parameter):
        key_name = parameter["key_name"]

        def select_by_key_name(key_name):
            try:
                KeyWords_info = db_session.query(KeyWords).filter(KeyWords.key_name == key_name).first()
                return KeyWords_info.single_to_dict()
            except:
                return []

        result = select_by_key_name(key_name)
        if len(result) != 0:
            return {"code": "400", "message": "关键词名重复"}
        else:
            key_word = KeyWords()
            key_word.key_name = key_name
            datetime_str = time.strftime('%Y-%m-%d %H', time.localtime(time.time()))
            key_word.pid = int(time.time())
            key_word.create_time = datetime_str
            try:
                db_session.add(key_word)
                db_session.commit()
                db_session.close()
                return {"code": "200", "message": "添加成功"}
            except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
                db_session.close()
                return {"code": "400", "message": "添加失败"}

    @classmethod
    @db_commit_decorator
    def update_word_list(cls, parameter):

        id = int(parameter['id'])
        remark = parameter['word_list']
        word_list = db_session.query(WordList).filter(WordList.id == id).first()
        try:
            word_list.word_list = str(remark)
            db_session.commit()
            db_session.close()
            return {"code": "200", "message": "succeed", }
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}

    @classmethod
    @db_commit_decorator
    def delete_word_list_by_id(cls, parameter):

        try:
            keyAndTemplate = db_session.query(KeyAndTemplate).filter(KeyAndTemplate.word_list_id == int(parameter['id'])).first()
            db_session.delete(keyAndTemplate)
            db_session.commit()
            word_list = db_session.query(WordList).filter(WordList.id == int(parameter['id'])).first()
            db_session.delete(word_list)
            db_session.commit()
            db_session.close()
            return {"code": "200", "message": "succeed", }
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}

    @classmethod
    @db_commit_decorator
    def add_word_list_by_key_id(cls, parameter):

        pid = int(parameter['pid'])
        word_list = WordList()
        word_list.key = parameter["key"]
        word_list.pid = pid
        try:
            db_session.add(word_list)
            db_session.commit()
            db_session.close()
            return {"code": "200", "message": "succeed", }
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}


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
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}
        try:
            status = parameter['status']
            mainurl.status = status
            db_session.commit()
            db_session.close()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}
        try:
            rule = parameter['rule']
            mainurl.rule = rule
            db_session.commit()
            db_session.close()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}

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
        mainurl.sort = parameter['sort']
        db_session.add(mainurl)
        db_session.commit()
        db_session.close()

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
    @db_commit_decorator
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

            return {"code": "200", "message": "succeed", "data": [item.single_to_dict() for item in datas],
                    "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}


class SpiderTaskOper:

    @classmethod
    @db_commit_decorator
    def update_status(cls, parameter):
        spider_task = db_session.query(SpiderTask).filter(
            SpiderTask.id == int(parameter["id"])).first()
        spider_task.status = int(parameter["status"])
        db_session.commit()
        db_session.close()

    @classmethod
    @db_commit_decorator
    def start_task(cls, parameter):
        spider_name = int(parameter['id'])
        datas = db_session.query(MainUrl).filter(MainUrl.spider_name == spider_name, MainUrl.status == 1).all()
        db_session.close()
        parameters = []
        for item in [item.single_to_dict() for item in datas]:
            parameter = {}
            url = item.get("address")
            try:
                rule = item["rule"]
                if rule == None or rule == "null" or rule == "":
                    crawler_info.info("{} : has no filtering rules, default algorithm acquisition".format(url))
                    parameter["rule"] = {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                                         'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}
                else:
                    filter_rule = json.loads(rule)["filter_rule"]
                    if filter_rule and filter_rule != "":
                        rule = json.loads(item["rule"].replace("@", "+"))
                        parameter["rule"] = rule
                    else:
                        parameter["rule"] = rule
            except:
                crawler_info.info("{} : has no filtering rules, default algorithm acquisition".format(url))
                parameter["rule"] = {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                                     'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}

            parameter["pid"] = item.get("pid")
            parameter["webSite"] = item.get("webSite")
            parameter["url"] = str(url).strip()
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
        spider_task.status = 0
        spider_task.creater = 'admin'
        spider_task.create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        db_session.add(spider_task)

        db_session.commit()
        db_session.close()
        return {"code": "200", "message": "succeed"}

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

            return {"code": "200", "message": "succeed", "data": [item.single_to_dict() for item in datas],
                    "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}


class TaskConfigOper:

    @classmethod
    @db_commit_decorator
    def select_by_id(cls, parameter):

        spider_name = int(parameter['id'])
        page = int(parameter['page'])
        limit = int(parameter['limit'])
        try:
            datas = db_session.query(MainUrl).filter(MainUrl.spider_name == spider_name, MainUrl.status == 1).limit(
                limit).offset(
                (page - 1) * limit)
            count = db_session.query(MainUrl).filter(MainUrl.spider_name == spider_name, MainUrl.status == 1).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data": [item.single_to_dict() for item in datas],
                    "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    @classmethod
    @db_commit_decorator
    def select_all(cls, parameter):

        page = int(parameter['page'])
        limit = int(parameter['limit'])
        sort = int(parameter['sort'])

        try:
            datas = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.spider_name == 0,
                                                     MainUrl.status == 1).limit(
                limit).offset(
                (page - 1) * limit)
            count = db_session.query(MainUrl).filter(MainUrl.sort == sort, MainUrl.spider_name == 0,
                                                     MainUrl.status == 1).count()
            db_session.close()

            return {"code": "200", "message": "succeed", "data": [item.single_to_dict() for item in datas],
                    "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    # parameter ={"task_id":1 ,"operation":"import","main_url_pids":[6571,4541,45781,1512]}
    @classmethod
    @db_commit_decorator
    def update_task_name(cls, parameter):

        spider_name = int(parameter['task_id'])
        main_url_pids = parameter['main_url_pids']
        operation = str(parameter['operation'])
        if main_url_pids != "":
            try:
                if operation == "import":
                    for main_url_pid in eval(main_url_pids):
                        main_url = db_session.query(MainUrl).filter(
                            MainUrl.pid == main_url_pid).first()
                        main_url.spider_name = spider_name
                elif operation == "remove":
                    for main_url_pid in eval(main_url_pids):
                        main_url = db_session.query(MainUrl).filter(
                            MainUrl.pid == main_url_pid).first()
                        main_url.spider_name = 0
                db_session.commit()
                db_session.close()
                return {"code": "200", "message": "更新成功"}

            except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
                db_session.close()
                return {"code": "404", "message": "更新失败"}
        else:
            return {"code": "202", "message": "并没有移除数据"}


keyword = KeyWordsOper()


class TemplateOper:

    @classmethod
    @db_commit_decorator
    def select_by_parameter(cls, parameter):

        page = int(parameter['page'])
        limit = int(parameter['limit'])
        status = int(parameter['status'])
        try:
            datas = db_session.query(Template).filter(Template.status == status).limit(
                limit).offset(
                (page - 1) * limit)
            count = db_session.query(Template).filter(Template.status == status).count()

            db_session.close()

            return {"code": "200", "message": "succeed", "data": [item.single_to_dict() for item in datas],
                    "count": count}

        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed", "data": [], "count": 0}

    @classmethod
    @db_commit_decorator
    def select_remove_template(cls, parameter):
        try:
            result_all = cls.select_by_parameter(parameter)
            result = keyword.select_by_id(parameter)
            data_pid = result["data"]["word_list"]
            data_page = result_all["data"]
            for jtem in data_pid:
                for item in data_page:
                    if item["id"] == jtem["key_id"]:
                        item["exist"] = 1
            for item in data_page:
                if "exist" not in str(item):
                    item["exist"] = 0
            return {"code": "200", "message": "succeed", "data": data_page,
                    "count": result_all["count"]}
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            return {"code": "404", "message": "fialed", "data": [], "count": 0}


class KeyAndTemplateOper:

    @classmethod
    @db_commit_decorator
    def add_list(cls, parameter):
        template_id_list = parameter["template_id_list"].split(",")
        key_id = parameter["key_id"]
        try:
            for template_id in template_id_list:
                cls.add_one(key_id, template_id)
            db_session.commit()
            db_session.close()
            return {"code": "200", "message": "succeed"}
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.rollback()
            db_session.close()
            return {"code": "404", "message": "fialed"}

    @classmethod
    @db_commit_decorator
    def add_one(cls, key_id, template_id):
        try:
            Template_info = db_session.query(Template).filter(
                Template.id == template_id).first()
            template_name = Template_info.single_to_dict()["template_name"]
            wordlist = WordList()
            wordlist.key = template_name
            pid = int(time.time() * 1000)
            wordlist.pid = pid
            db_session.add(wordlist)
            db_session.commit()
            word_info = db_session.query(WordList).filter(
                WordList.pid == pid).first()
            key_and_template = KeyAndTemplate()
            key_and_template.key_id = key_id
            key_and_template.template_id = template_id
            key_and_template.word_list_id = word_info.id
            db_session.add(key_and_template)
            db_session.commit()
            db_session.close()
            return {"code": "200", "message": "succeed"}
        except (SqlalchemyIntegrityError, PymysqlIntegrityError, InvalidRequestError):
            db_session.close()
            return {"code": "404", "message": "fialed"}


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
    # spider = TaskConfigOper()
    # # parameter = {
    # #         "page":2,
    # #         "limit":10,
    # #         "sort":0
    # #     }
    # # print(spider.select_all(parameter))
    # parameter = {
    #         "id":1
    #     }
    # print(spider.select_by_id(parameter))
    #     # spider.add_one(parameter)
    info = '''
    {  
        'code': '200', 
        'message': 'succeed', 
        'data': {
                    'id': 1,
                    'key_name':'test', 
                    'pid': 23,
                    'create_time': datetime.datetime(2020, 4, 23, 9, 28, 57), 
                    'word_list': [
                                    {
                                        id': 53,
                                        'pid': 23, 
                                        'word_list': ['', '啊沙发', '富士达', '嘎嘎嘎', '111', '222', '333', '4444444444', '55555555555', '77777777', '8888888888888'], 
                                        'key': '是的冯绍峰'
                                    }, 

                                    {
                                        'id': 91, 
                                        'pid': 23,
                                        'word_list': [''],
                                        'key': '十多个富士达'}
                                ] 
                },
        'count': 1}

    '''
    # print(info)
    spider_task = KeyWordsOper()
    parameter = {"key_id": 2, 'template_id_list': "1,7,8,4", "id": 19, 'page': 2, 'limit': 5, 'status': 1}
    print(spider_task.delete_by_id(parameter))
    # parameter = {
    #             "id":27,
    #         }
    # result = spider_task.start_task(parameter)
    # print(result)
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
