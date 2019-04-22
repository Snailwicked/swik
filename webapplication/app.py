from __future__ import unicode_literals
from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user
from webapplication.forms import TodoListForm, LoginForm
from webapplication.ext import db, login_manager
from webapplication.models import WebInfo, User
from flask_nav import Nav
from flask_nav.elements import *


SECRET_KEY = 'This is my key'
app = Flask(__name__)
bootstrap = Bootstrap(app)
nav = Nav()
nav.register_element('top', Navbar(u'爬虫管理后台',
                                    View(u'主页', 'show_todo_list'),
                                    View(u'网址管理', 'show_todo_list'),
                                    Subgroup(u'爬虫管理',
                                             View(u'在启动爬虫列表', 'show_todo_list'),
                                             Separator(),
                                             View(u'待启动爬虫列表', 'show_todo_list'),
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


@app.route('/', methods=['GET', 'POST'])
@login_required
def show_todo_list():
    form = TodoListForm()
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        pagination = WebInfo.query.order_by(WebInfo.add_time.desc()).paginate(page, per_page=10, error_out=False)
        webinfos = pagination.items
        # webinfos = WebInfo.query.all()
        return render_template('index.html', webinfos=webinfos, form=form, pagination=pagination)
    if form.validate_on_submit():
        webinfo = WebInfo(form.url.data, form.web_name.data, form.status.data, form.agent.data, form.sort.data)
        db.session.add(webinfo)
        db.session.commit()
        flash('您已成功添加')
    else:
        flash(form.errors)
    return redirect(url_for('show_todo_list'))


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
@login_required
def delete_todo_list(id):
    webinfo = WebInfo.query.filter_by(id=id).first()
    db.session.delete(webinfo)
    db.session.commit()
    flash('您已成功删除')
    return redirect(url_for('show_todo_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username'], password=request.form['password']).first()
        if user:
            login_user(user)
            flash('您已登录!')
            return redirect(url_for('show_todo_list'))
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


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
