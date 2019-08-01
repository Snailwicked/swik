from flask import Flask, request, jsonify,render_template
from flask_cors import *
from db.dao import MainUrlOper,WebInfoOper
from webapplication.service.spider_tasks.task_add import TaskAdd
from webapplication.service.spider_tasks.task_select import TaskSelect
from webapplication.service.spider_tasks.task_update import TaskUpdate
from webapplication.service.spider_tasks.task_delete import TaskDelete
from webapplication.service.spider_tasks.task_config_update import TaskConfigUpdate
import json
webinfo = WebInfoOper()
mainurl = MainUrlOper()

SECRET_KEY = 'This is the key'
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = SECRET_KEY

data = []
news = []

########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''

@app.route('/json/test')
def json_test():
    json = {
        'page': 10,
        'good_list': "//ul[@id= 'newsListContent']//li//p[@class='title']//a//@href",
        'domain': 'http://stock.eastmoney.com/a/cdpfx_{}.html',
        "content_xpath": {
            'personnel_title': '//h1//text()',
            'attendance_time': '//div[@class="time"]//text()',
        },
        'author': 'snail'}
    return jsonify(json)


########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''
@app.route('/task/add')
def add_task():
    add = TaskAdd()
    task_name = request.values.to_dict()
    add.add_task(task_name)
    return "1"


@app.route('/task/delete')
def delete_task():
    delete = TaskDelete()
    params = request.values.to_dict()
    delete.delete_one(params)
    return jsonify({"code": 1, "msg": "删除成功"})

@app.route('/task/select')
def select_tasks():
    select = TaskSelect()
    params = request.values.to_dict()

    data = select.select_task(params)
    return jsonify({"code": 0, "msg": "", "count": data['count'], "data": data['data']})


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

@app.route('/task_config/select')
def select_task_config():
    select = TaskSelect()
    params = request.values.to_dict()
    data = select.select_task_config(params)
    return jsonify({"code": 0, "msg": "",  "data": data[0]})


@app.route('/task_config/update')
def update_task_config():
    update = TaskConfigUpdate()
    params = request.values.to_dict()
    data = update.update(params)
    return jsonify({"code": 0, "msg": "",  "data": data})

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

@app.route('/web_site/update')
def update_web_site():
    parameter = request.args.to_dict()
    mainurl.update_mainurl(parameter)
    return jsonify({"code": 0, "msg": "更新成功"})




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
