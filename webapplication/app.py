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
from celery import Celery


import json
from utils.spiderutils.parse import Parse



from webapplication.service.celery_task.task_spider import add
from celery.result import AsyncResult


SECRET_KEY = 'This is the key'
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = SECRET_KEY


app.config['CELERY_BROKER_URL'] = 'redis://101.132.113.50:6379/2'
app.config['CELERY_RESULT_BACKEND'] = 'redis://101.132.113.50:6379/3'
app.config['CELERY_TASK_SERIALIZER'] = 'json'
app.config['CELERY_RESULT_SERIALIZER'] = 'json'
app.config['CELERY_ACCEPT_CONTENT'] = ["json"]
celery = Celery('tasks', broker=app.config['CELERY_BROKER_URL'], backend=app.config['CELERY_RESULT_BACKEND'])


celery.conf.update(app.config)



data = []
news = []



########################################################################################################################
'''
    站点模块代码
    get_tasks_on：  更新站点站点子类信息

'''
@celery.task(name='app.async_crawl')
def async_crawl(url):
    parse = Parse()
    result = parse.get_data(url)
    return result


@celery.task(name='app.async_task')
def async_task(uuid):
    """
    :param uuid: 通过uuid 获取mongdb数据库中的url 进行采集
    :return:
    """
    print(uuid)
    pass




@app.route('/task/test')
def tasks_test():
    params = request.values.to_dict()
    urls = params.get("url")
    task = async_crawl.apply_async(eval(urls))
    # parse = Parse()
    # data = parse.get_data(urls)
    return jsonify({"code": 0, "msg": "", "task_id": task.id})



@app.route('/task/result')
def result_task():
    params = request.values.to_dict()
    task_id = params.get("task_id")
    result = async_crawl.AsyncResult(task_id).get()
    return str(result)

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



@app.route('/task/start')
def tasks_start():
    params = request.values.to_dict()
    uuid = params.get("uuid")
    task = async_task.apply_async(uuid)
    return jsonify({"code": 0, "msg": "成功启动", "task_id": task.id})

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
