from flask import Flask, request, jsonify
from config import *
from flask_cors import *
from tasks.accurate_crawler import Crawleruning
from tasks import excute_start_crawler
from utils.base_utils.system import System
from db import News_data
from db.dao import MainUrlOper
from db.dao import TaskConfigOper
from db.dao import SpiderTaskOper
from db.dao import KeyWordsOper
from db.dao import TemplateOper
from db.dao import KeyAndTemplateOper
from spiders import *
con = News_data()
import json
mainurl = MainUrlOper()
taskconfig = TaskConfigOper()
spidertask = SpiderTaskOper()
keyword = KeyWordsOper()
template = TemplateOper()
keyandtemplate = KeyAndTemplateOper()

system = System()
SECRET_KEY = 'This is the key'
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = SECRET_KEY
data = []
news = []

@app.route('/system/info')
def system_info():
    return jsonify(system.infos())


@app.route('/new/datas')
def new_datas():
    parameter = request.values.to_dict()
    result = con.select_by_paramters(parameter)
    return jsonify(result)


@app.route('/new/delete')
def new_delete():
    parameter = request.values.to_dict()
    print(parameter)
    # result = con.select_by_paramters(parameter)
    return jsonify(parameter)

########################################################################################################################
'''
    模板配置
    get_tasks_on：  更新站点站点子类信息
'''
@app.route('/key_select_template/add')
def key_select_template():
    parameter = request.values.to_dict()
    data = keyandtemplate.add_list(parameter)
    return jsonify(data)

########################################################################################################################
'''
    关键词模块
    get_tasks_on：  更新站点站点子类信息
'''
@app.route('/template/select')
def select_template():
    parameter = request.values.to_dict()
    data = template.select_by_parameter(parameter)
    return jsonify(data)

@app.route('/template/select_remove')
def select_remove_template():
    parameter = request.values.to_dict()
    data = template.select_remove_template(parameter)
    return jsonify(data)

########################################################################################################################
'''
    关键词模块
    get_tasks_on：  更新站点站点子类信息
'''
@app.route('/key_words/select')
def select_key_words():
    parameter = request.values.to_dict()
    data = keyword.select_by_parameter(parameter)
    return jsonify(data)

@app.route('/key_words/delete_by_id')
def delete_key_words_by_id():
    parameter = request.values.to_dict()
    data = keyword.delete_by_id(parameter)
    return jsonify(data)

@app.route('/key_words/select_by_id')
def select_key_words_by_id():
    parameter = request.values.to_dict()
    data = keyword.select_by_id(parameter)
    return jsonify(data)

@app.route('/word_list/update_by_id')
def update_words_list_by_id():
    parameter = request.values.to_dict()
    data = keyword.update_word_list(parameter)
    return jsonify(data)

@app.route('/word_list/delete_word_list_by_id')
def delete_word_list_by_id():
    parameter = request.values.to_dict()
    data = keyword.delete_word_list_by_id(parameter)
    return jsonify(data)
@app.route('/word_list/add_word_list_by_key_id')
def add_word_list_by_key_id():
    parameter = request.values.to_dict()
    data = keyword.add_word_list_by_key_id(parameter)
    return jsonify(data)

@app.route('/key_words/add_key_word')
def add_key_word():
    parameter = request.values.to_dict()
    data = keyword.add_key_word(parameter)
    return jsonify(data)
########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''
@app.route('/task/add')
def add_task():
    parameter = request.values.to_dict()
    result = spidertask.add_one(parameter)
    return jsonify(result)


@app.route('/task/delete')
def delete_task():
    parameter = request.values.to_dict()
    spidertask.delete_one(parameter)
    return jsonify({"code": 1, "msg": "删除成功"})

@app.route('/task/select')
def select_tasks():
    parameter = request.values.to_dict()
    data = spidertask.select_by_parameter(parameter)
    return jsonify(data)

########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''

@app.route('/task_config/select_by_id')
def select_task_config_by_id():
    parameter = request.values.to_dict()
    data = taskconfig.select_by_id(parameter)
    return jsonify(data)

@app.route('/task_config/select_all')
def select_all_task_config():
    parameter = request.values.to_dict()
    data = taskconfig.select_all(parameter)
    return jsonify(data)

@app.route('/task_config/spider_name')
def task_config_spider_name():
    parameter = request.values.to_dict()
    data = taskconfig.update_task_name(parameter)
    return jsonify(data)


@app.route('/start/spider_task')
def start_spider_task():
    parameter = request.values.to_dict()
    parameter["status"] = 1
    spidertask.update_status(parameter)
    task_id = excute_start_crawler(parameter)
    return jsonify({"task_id":task_id})

@app.route('/start/spider_accurate')
def start_spider_accurate():
    # parameter = request.values.to_dict()
    # data = keyword.select_by_id(parameter)
    # for item in data["data"]["word_list"]:
    #     if item["path"] =="weibo":
    #         config = {"page":3,"key_words":["央视新闻"]}
    #         weibo = WeiBo_Spider(config)
    #         weibo.start()
        # print(item["path"])
        # print(item["word_list"])

    # spidertask.update_status(parameter)
    # task_id = excute_start_crawler(parameter)
    return jsonify({"task_id":""})

@app.route('/stop/spider_task')
def stop_spider_task():
    from db.redis_db import Clear_Con
    clear_con = Clear_Con()
    parameter = request.values.to_dict()
    parameter["status"] = 0
    spidertask.update_status(parameter)
    clear_con.clear()
    return jsonify({"task_id":""})

########################################################################################################################
'''
    站点模块代码
    update_web_site：  更新站点站点子类信息
    select_web_site：  查询站点站点子类信息

'''
@app.route('/web_site/select_all')
def select_web_site():
    parameter = request.args.to_dict()
    data = mainurl.select_by_parameter(parameter)
    return jsonify(data)

@app.route('/web_site/delete')
def delete_web_site():
    parameter = request.args.to_dict()
    mainurl.delete_one(parameter)
    return ""

@app.route('/web_site/add')
def add_web_site():
    parameter = request.args.to_dict()
    mainurl.add_one(parameter)
    return ""

@app.route('/web_site/update')
def update_web_site():
    parameter = request.args.to_dict()
    mainurl.update_mainurl(parameter)
    return jsonify({"code": 0, "msg": "更新成功"})

@app.route('/web_site/spider')
def spider_web_site():
    from tasks.test_parse import Parse
    parse = Parse()
    parameter = request.args.to_dict()
    parameter["url"] = str(parameter["url"]).strip()
    parameter["webSite"] ="测试"

    if parameter["rule"] == "null":
        parameter["rule"] = {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                         'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}
    else:
        parameter["rule"] = json.loads(parameter["rule"])
    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()
    target_url = crawler.process()
    for sub_url in target_url:
        parameter["url"] = sub_url
        parse.get_data(parameter)
    return crawler.monitor_info()

if __name__ == '__main__':
    crawler_info.info("If you do not see the data, enter 'celery -A workers.app worker -l info -P eventlet' on the command line")
    crawler_info.info("If you do not see the data, enter 'celery -A tasks.workers.app worker -l info -P eventlet' on the command line")

    # app.run(host='192.168.4.2',port=5001)

    app.run(debug=True,port=5000)
