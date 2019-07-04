from flask import Flask, request, jsonify,render_template
from flask_cors import *
from webapplication.service.spider_domain.domain_select import DomainSelect
from webapplication.service.spider_domain.domain_update import DomainUpdate


from webapplication.service.spider_webs.web_add import WebAdd
from webapplication.service.spider_webs.web_delete import WebDelete
from webapplication.service.spider_webs.web_update import WebUpdate
from webapplication.service.spider_webs.web_select import WebSelect


from webapplication.service.spider_tasks.task_add import TaskAdd
from webapplication.service.spider_tasks.task_select import TaskSelect
from webapplication.service.spider_tasks.task_update import TaskUpdate
from webapplication.service.spider_tasks.task_delete import TaskDelete

from webapplication.service.spider_tasks.task_config_update import TaskConfigUpdate


import json
from utils.spiderutils.parse import Parse
import threading

# from celery import Celery


SECRET_KEY = 'This is the key'
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = SECRET_KEY
# cele = Celery('app', app.config['CELERY_BROKER_URL'])
# cele.config_from_object('celery_config')
data = []
news = []

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
    # update = TaskUpdate()
    parse = Parse()
    # data = request.values().decode('utf-8')
    # update.update_status(json.loads(data))
    # update_other = TaskUpdate()
    # urls = update_other.query_mongo_urls(json.loads(data))
    urls = []
    urls.append(params.get("url"))
    print(len(urls))
    data = parse.get_data(urls)
    return jsonify({"code": 0, "msg": "", "count": len(data), "data": data})

########################################################################################################################
'''
    站点模块代码
    update_web_site：  更新站点站点子类信息
    select_web_site：  查询站点站点子类信息

'''
@app.route('/web_site/select_all')
def select_web_site():
    select = DomainSelect()
    params = request.args.to_dict()
    print(request.url)
    print(params)
    data = select.select_all(params)
    return jsonify({"code": 0, "msg": "", "count": data['count'], "data": data['data']})

@app.route('/web_site/update')
def update_web_site():
    update = DomainUpdate()
    params = request.args.to_dict()
    print(request.url)
    update.update(params)
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
    select = WebSelect()
    params = request.args.to_dict()
    print(params)
    data = select.select_all(params)
    print(data)
    return jsonify({"code": 0, "msg": "", "count": data['count'], "data": data['data']})


@app.route('/web/delete', methods=["POST"])
def delete_sub_web():
    delete = WebDelete()
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        delete.delete_one(json.loads(data))
    return jsonify({"code": 1, "msg": "删除成功"})


@app.route('/web/add', methods=["POST"])
def add_sub_web():
    add = WebAdd()
    if request.method == 'POST':
        web_name = request.form['web_name']
        web_url = request.form['web_url']
        agent = request.form['agent']
        sort = request.form['sort']
        add.add_one({"web_name": web_name, "web_url": web_url, "agent": agent, "sort": sort})
    return "1"


@app.route('/web/update')
def update_sub_web():
    update = WebUpdate()
    data = request.values.to_dict()
    print(data)
    update.update(data)
    return jsonify({"code": 1, "msg": "更新成功"})


if __name__ == '__main__':
    app.run(debug=True)
