from flask import Flask, request, jsonify
from config import *
from flask_cors import *
from db.dao import MainUrlOper,SpiderTaskOper,TaskConfigOper
from tasks.crawler import Crawleruning
from tasks import excute_start_crawler
from utils.base_utils.system import System
from db import News_data
con = News_data()
import json
mainurl = MainUrlOper()
taskconfig = TaskConfigOper()
spidertask = SpiderTaskOper()
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
    parameter = request.args.to_dict()
    parameter["url"] = str(parameter["url"]).strip()

    if parameter["rule"] == "null":
        parameter["rule"] = {'filter_rule': '', 'selector': 'xpath', 'deep_limit': '1',
                         'fields': {'title': '', 'author': '', 'publishTime': '', 'content': ''}}
    else:
        parameter["rule"] = json.loads(parameter["rule"].replace("@","+"))

    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()
    result = crawler.monitor_info()
    return jsonify(result)



if __name__ == '__main__':
    crawler_info.info("If you do not see the data, enter 'celery -A tasks.workers.app worker -l info -P eventlet' on the command line")
    app.run(debug=True)
'''
http://news.cyol.com/app/2019-08/24/content_18127145.htm
http://news.cyol.com/app/\d[5]-\d[2]/\d[2]/content_+d+.htm

'''