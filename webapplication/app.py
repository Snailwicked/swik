from __future__ import unicode_literals
from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user
from webapplication.forms import TodoListForm, LoginForm, WaitedTaskForm, SearchForm
from webapplication.ext import db, login_manager
from webapplication.models import WebInfo, User, SpiderTask
from flask_nav import Nav
from flask_nav.elements import *
from datetime import datetime
from flask_pymongo import PyMongo
from utils.spiderutils.parse import Parse
import json
'''
后台管理的视图函数
author: 王凯
datetime: 2019/04/24
'''
SECRET_KEY = 'This is my key'
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://101.132.113.50:27017/spider_manage"
mongo = PyMongo(app)
bootstrap = Bootstrap(app)
nav = Nav()
nav.register_element('top', Navbar(u'爬虫管理后台',
                                    View(u'主页', 'index'),
                                   Subgroup(u'网址管理',
                                            View(u'在采集网址管理', 'doing_crawler'),
                                            Separator(),
                                            View(u'待采集网址管理', 'show_todo_list'),
                                            Separator(),
                                            View(u'问题网址管理', 'show_todo_list'),
                                            )
                                   ,
                                    Subgroup(u'爬虫管理',
                                             View(u'在启动爬虫任务列表', 'show_todo_list'),
                                             Separator(),
                                             View(u'待启动爬虫任务列表', 'show_waited_task'),
                                    ),
                                    Subgroup(u'数据统计',
                                            View(u'服务器监控', 'show_todo_list'),
                                            Separator(),
                                            View(u'爬虫监控', 'show_todo_list'),
                                            ),
                                    View(u'权限管理', 'show_todo_list'),
))
nav.init_app(app)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:BlueSnail123!@101.132.113.50/spider_manage"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/SearchWeb', methods=['GET', 'POST'])
@login_required
def search_web():
    if request.method == "POST":
        form = TodoListForm()
        search_form = SearchForm()
        page = request.args.get('page', 1, type=int)
        web_name = request.form.get('search_name')
        pagination = WebInfo.query.filter(WebInfo.web_name.contains(web_name)).order_by(WebInfo.add_time.desc()).\
            paginate(page, per_page=15, error_out=False)
        webinfos = pagination.items
        return render_template('waited_crawler.html', webinfos=webinfos, form=form, search_form=search_form,
                               pagination=pagination)
    return redirect(url_for('show_todo_list'))


@app.route('/DoingCrawler', methods=['GET', 'POST'])
@login_required
def doing_crawler():
    form = TodoListForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = WebInfo.query.filter_by(status=1).order_by(WebInfo.add_time.desc()).paginate(page, per_page=15,
                                                                                                  error_out=False)
        webinfos = pagination.items
        # webinfos = WebInfo.query.all()
        return render_template('doing_crawler.html', webinfos=webinfos, form=form, pagination=pagination)
    if form.validate_on_submit():
        webinfo = WebInfo(form.url.data, form.web_name.data, form.status.data, form.agent.data,
                          form.sort.data)
        db.session.add(webinfo)
        db.session.commit()
        flash('您已成功添加')
    elif form.validate_on_submit():
        if form.start_time and form.search_name:
            results = WebInfo.query.filter_by(web_name=form.search_name.data)
            if results:
                return render_template('doing_crawler.html', form=form)
            else:
                flash("没有查询到数据")
        elif form.start_time and not form.search_name:
            results = WebInfo.query.filter(WebInfo.add_time.between(datetime.strftime(form.start_time.data)),
                                           datetime.strftime(form.end_time.data))
            if results:
                return render_template('doing_crawler.html', form=form)
            else:
                flash("没有查询到数据")
        elif not form.start_time and form.search_name:
            results = WebInfo.query.filter_by(web_name=form.search_name.data)
            if results:
                return render_template('doing_crawler.html', form=form)
            else:
                flash("没有查询到数据")
    else:
        flash(form.errors)
    return redirect(url_for('doing_crawler'))


@app.route('/WebWaitedShow', methods=['GET', 'POST'])
@login_required
def show_todo_list():
    search_form = SearchForm()
    form = TodoListForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = WebInfo.query.filter_by(status=0).order_by(WebInfo.add_time.desc()).paginate(page, per_page=15,
                                                                                                  error_out=False)
        webinfos = pagination.items
        # webinfos = WebInfo.query.all()
        return render_template('waited_crawler.html', webinfos=webinfos, form=form, pagination=pagination, search_form=search_form)
    if form.validate_on_submit():
        webinfo = WebInfo(form.url.data, form.web_name.data, form.status.data, form.agent.data,
                          form.sort.data)
        db.session.add(webinfo)
        db.session.commit()
        flash('您已成功添加')
    elif form.validate_on_submit():
        if form.start_time and form.search_name:
            results = WebInfo.query.filter_by(web_name=form.search_name.data)
            if results:
                return render_template('waited_crawler.html', form=form)
            else:
                flash("没有查询到数据")
        elif form.start_time and not form.search_name:
            results = WebInfo.query.filter(WebInfo.add_time.between(datetime.strftime(form.start_time.data)),
                                           datetime.strftime(form.end_time.data))
            if results:
                return render_template('waited_crawler.html', form=form)
            else:
                flash("没有查询到数据")
        elif not form.start_time and form.search_name:
            results = WebInfo.query.filter_by(web_name=form.search_name.data)
            if results:
                return render_template('waited_crawler.html', form=form)
            else:
                flash("没有查询到数据")
    else:
        flash(form.errors)
    return redirect(url_for('show_todo_list'))


@app.route('/TaskWaitedShow', methods=['POST', 'GET'])
@login_required
def show_waited_task():
    form = WaitedTaskForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = SpiderTask.query.filter_by(status=0).order_by(SpiderTask.create_time.desc()).\
            paginate(page, per_page=15, error_out=False)
        tasks = pagination.items
        task_mongo = mongo.db.config
        return render_template('waited_task.html', form=form, tasks=tasks, pagination=pagination)
    if form.validate_on_submit():
        waited_task = mongo.db.congif.insert_one({'limit': form.limit.data})
        if waited_task:
            flash("配置成功")
    else:
        flash(form.errors)
    return redirect(url_for('show_waited_task'))


@app.route('/DeleteWeb/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_todo_list(id):
    """
    单个删除网站
    :param id:
    :return:
    """
    webinfo = WebInfo.query.filter_by(id=id).first()
    db.session.delete(webinfo)
    db.session.commit()
    flash('您已成功删除')
    return redirect(url_for('show_todo_list'))


@app.route('/DeleteWebList', methods=['GET', 'POST'])
@login_required
def delete_todo_list2():
    """
    批量删除网站
    :return:
    """
    ids = request.form.get("ids")
    for id in ids:
        webinfo = WebInfo.query.filter_by(id=id).first()
        db.session.delete(webinfo)
        db.session.commit()
    flash("您已成功批量删除")
    return redirect(url_for('show_todo_list'))


@app.route('/DeleteTask/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_task(id):
    task = SpiderTask.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    flash("您已成功删除")
    return redirect(url_for('show_waited_task'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('您已登录!')
            return redirect(url_for('index'))
        else:
            flash('用户名或者密码不正确')
    form = LoginForm()
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已退出!')
    return redirect(url_for('login'))


@app.route('/')
@login_required
def index():
    return render_template('base.html')


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


@app.route('/StartSpider/<string:id>', methods=['GET', 'POST'])
@login_required
def run_spider(id):
    task = SpiderTask.query.filter_by(config_name=id).first()
    task.status = 1
    db.session.commit()
    parse = Parse()
    urls = mongo.db.config.find_one_or_404({'uuid': id})['urls']
    result = parse.get_data(urls)
    if result:
        flash('爬虫采集完毕')
    return redirect(url_for('show_waited_task'))


@app.route('/GetMongoDb/<string:id>', methods=['GET', 'POST'])
@login_required
def get_mongodb_config(id):
    config_all = mongo.db.config.find_one_or_404({'uuid': id})
    config_all.pop("_id")
    config_all.pop("uuid")
    return json.dumps(config_all)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
