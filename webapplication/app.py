from __future__ import unicode_literals
from flask import (Flask, render_template, redirect, url_for, request, flash)
from flask_bootstrap import Bootstrap
from flask_login import login_required, login_user, logout_user, current_user
from .forms import TodoListForm, LoginForm
from .ext import db, login_manager
from .models import WebInfo, User


SECRET_KEY = 'This is my key'
app = Flask(__name__)
bootstrap = Bootstrap(app)
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
        webinfos = WebInfo.query.all()
        return render_template('index.html', webinfos=webinfos, form=form)


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
