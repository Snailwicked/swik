from flask import Flask,request,jsonify
from flask_cors import *
from webapplication.service.spider_webs.select import Select
from webapplication.service.spider_webs.add import Add
from webapplication.service.spider_webs.delete import Delete
from webapplication.service.spider_webs.update import Update

import json

app = Flask(__name__)
CORS(app, supports_credentials=True)

data = []
news = []
# 启用网址
@app.route('/select_all')
def get_datas_on():
    select = Select()
    page = request.args.get('page')
    limit = request.args.get('limit')
    params = {'page': page, 'limit': limit}
    data = select.select_all(params)
    return jsonify({"code": 0, "msg": "", "count": data['count'], "data": data['data']})


@app.route('/select_off')
def get_datas_off():
    select = Select()
    page = request.args.get('page')
    limit = request.args.get('limit')
    params = {'page': page, 'limit': limit}
    data = select.select_off(params)
    return jsonify({"code": 0, "msg": "", "count": data['count'], "data": data['data']})


@app.route('/delete', methods=["POST"])
def delete_data():
    delete = Delete()
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        delete.delete_one(json.loads(data))
    return jsonify({"code": 1, "msg": "删除成功"})


@app.route('/add', methods=["POST"])
def add_data():
    add = Add()
    if request.method == 'POST':
        web_name = request.form['web_name']
        web_url = request.form['web_url']
        agent = request.form['agent']
        sort = request.form['sort']
        add.add_one({"web_name": web_name, "web_url": web_url, "agent": agent, "sort": sort})
    return "1"


@app.route('/update', methods=["POST"])
def update():
    update = Update()
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        update.update(json.loads(data))
    return jsonify({"code": 1, "msg": "更新成功"})


@app.route('/on', methods=["POST"])
def state_on():
    update = Update()
    if request.method == 'POST':
        data = request.get_data().decode('utf-8')
        update.update_status(json.loads(data))
    return jsonify({"code": 1, "msg": "更新成功"})


if __name__ == '__main__':
    app.run()
