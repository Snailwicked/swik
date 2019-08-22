from flask import Flask, request, jsonify
from flask_cors import *
from db.dao import MainUrlOper,WebInfoOper,SpiderTaskOper,TaskConfigOper
from webapplication.service.spider_tasks.task_update import TaskUpdate
from core.crawler import Crawleruning
from utils.base_utils.system import System
import json
webinfo = WebInfoOper()
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



########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''
@app.route('/task/add')
def add_task():
    parameter = request.values.to_dict()
    print(parameter)
    spidertask.add_one(parameter)
    return "1"


@app.route('/task/delete')
def delete_task():
    parameter = request.values.to_dict()
    spidertask.delete_one(parameter)
    return jsonify({"code": 1, "msg": "删除成功"})

@app.route('/task/select')
def select_tasks():
    parameter = request.values.to_dict()
    print(parameter)
    data = spidertask.select_by_parameter(parameter)
    return jsonify(data)


@app.route('/task/update', methods=['POST'])
def update_task():
    update = TaskUpdate()
    data = request.get_data().decode('utf-8')
    update.update(json.loads(data))
    return jsonify({"code": 1, "msg": "更新成功"})

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



########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''
@app.route('/task/spider')
def tasks_spider():
    params = request.values.to_dict()
    print(params)
    urls = []
    urls.append(params.get("url"))
    from tasks import task_check
    task_check.excute_check_task(urls)
    return jsonify({"code": 0, "msg": "任务已启动"})

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
    # parameter = {"pid":7406}
    mainurl.delete_one(parameter)
    return ""

@app.route('/web_site/add')
def add_web_site():
    parameter = request.args.to_dict()
    print(parameter)
    # parameter = {"address":"test","webSite":"test","sort":0}
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
    parameter["rule"] = json.loads(parameter["rule"].replace("@","+"))
    # print(parameter)
    # print(type(parameter))
    # print(parameter)
    # # parameter = {
    # #     "url": "https://www.legalweekly.cn/",
    # #     "rule": {'author': '', 'filter_rule': 'https://www.legalweekly.cn/\w+/\d+.html', 'page_size': '1',
    # #              'content': '', 'header': '', 'issueTime': ''},
    # # }
    # print(parameter)
    # print(type(parameter))

    crawler = Crawleruning()
    crawler.set_parameter(parameter)
    crawler.start()

    return jsonify({"code": 0, "msg": "更新成功"})

'''
http://jiangsu.sina.com.cn/news/m/2019-08-07/detail-ihytcitm7447402.shtml
https://www.legalweekly.cn/fzsb/16165.html
/https://www.legalweekly.cn/\w+\/d+.shtml/

'''

########################################################################################################################
'''
    站点子模块代码
    delete_sub_web：  删除站点子类
    add_sub_web：     新增站点子类
    update_sub_web：  更新站点站点子类信息
    select_sub_web：  查询站点站点子类信息

'''
@app.route('/web/select_all')
def select_sub_web():
    parameter = request.args.to_dict()
    data = webinfo.select_by_parameter(parameter)
    print(data)
    return jsonify(data)


@app.route('/web/delete')
def delete_sub_web():
    parameter = request.values.to_dict()
    webinfo.delete_one(parameter)
    return jsonify({"code": 1, "msg": "删除成功"})


@app.route('/web/add')
def add_sub_web():
    parameter = request.values.to_dict()
    id = webinfo.add_one(parameter)
    return jsonify({"code": 1, "msg": "添加成功","id":id})


@app.route('/web/update')
def update_sub_web():
    parameter = request.values.to_dict()
    webinfo.update_webinfo(parameter)
    return jsonify({"code": 1, "msg": "更新成功"})

if __name__ == '__main__':
    app.run(debug=True)
